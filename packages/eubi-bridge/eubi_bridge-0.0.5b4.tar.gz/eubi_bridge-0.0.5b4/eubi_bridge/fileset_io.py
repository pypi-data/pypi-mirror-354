import sys
import tifffile
import copy, glob, re, os, itertools
from pathlib import Path
import dask.array as da, numpy as np, dask
from typing import Iterable, Callable, Union, List, Tuple
from natsort import natsorted

from eubi_bridge.ngff import defaults

transpose_list = lambda l: list(map(list, zip(*l)))
get_numerics = lambda string: list(re.findall(r'\d+', string))
get_alpha = lambda string: ''.join([i for i in string if not i.isnumeric()])


def get_matches(pattern, strings, return_non_matches=False):
    """
    Search for regex pattern matches in a list of strings.
    
    Args:
        pattern (str): Regular expression pattern to search for.
        strings (list): List of strings to search within.
        return_non_matches (bool): If True, returns all results including None for non-matches.
                                 If False, returns only successful matches.
    
    Returns:
        list: List of match objects (or None for non-matches if return_non_matches is True).
    """
    matches = [re.search(pattern, string) for string in strings]
    if return_non_matches:
        return matches
    return [match for match in matches if match is not None]


def split_by_match(filepaths, *args):
    """
    Group filepaths based on matching patterns.
    
    Args:
        filepaths (list): List of file paths to search in.
        *args: Variable number of patterns to search for in filepaths.
    
    Returns:
        dict: Dictionary with patterns as keys and lists of matching filepaths as values.
    """
    ret = dict().fromkeys(args)
    for key in args:
        matches = get_matches(key, filepaths)
        ret[key] = matches
    return ret


def find_match_and_numeric(filepaths, *args):
    """
    Find matches in filepaths and group them by their numeric suffixes.
    
    Args:
        filepaths (list): List of file paths to search in.
        *args: Variable number of patterns to search for in filepaths.
    
    Returns:
        dict: Dictionary where keys are matched patterns and values are lists of match objects.
    """
    ret = {}
    for key in args:
        matches = get_matches(key, filepaths)
        for match in matches:
            span = match.string[match.start():match.end()]
            if span not in ret.keys():
                ret[span] = [match]
            else:
                ret[span].append(match)
    return ret


def concatenate_shapes_along_axis(shapes: Iterable,
                                  axis: int
                                  ) -> list:
    """
    Concatenate shapes along a specified axis.
    
    Args:
        shapes (Iterable): Iterable of shape tuples to concatenate.
        axis (int): Axis along which to concatenate shapes.
    
    Returns:
        list: New shape after concatenation along the specified axis.
    
    Raises:
        ValueError: If dimensions other than the concatenation axis don't match.
    """
    reference_shape = shapes[0]
    concatenated_shape = [num for num in reference_shape]
    for shape in shapes[1:]:
        for idx, size in enumerate(shape):
            if idx == axis:
                concatenated_shape[idx] += size
            else:
                assert size == reference_shape[idx], ValueError(
                    "For concatenation to succeed, all dimensions except the dimension of concatenation must match.")
    return concatenated_shape


def accumulate_slices_along_axis(shapes: Iterable,
                                 axis: int,
                                 slices: Union[tuple, list] = None
                                 ) -> list:
    """
    Calculate accumulated slices for concatenation along a specified axis.
    
    Args:
        shapes (Iterable): Iterable of shape tuples to be concatenated.
        axis (int): Axis along which to calculate slices.
        slices (Union[tuple, list], optional): Initial slices. If None, creates full slices.
    
    Returns:
        list: List of slice tuples for each input shape.
    """
    reference_shape = shapes[0]
    if slices is None:
        slices = [[slice(None, None) for _ in reference_shape] for _ in shapes]
    assert (len(shapes) == len(slices))
    sizes_per_axis = [shape[axis] for shape in shapes]
    cummulative_sizes = [0] + np.cumsum(sizes_per_axis).tolist()
    slice_tuples = [(cummulative_sizes[idx], cummulative_sizes[idx + 1]) for idx in range(len(sizes_per_axis))]
    for idx, tup in enumerate(slice_tuples):
        slc = slices[idx]
        slclist = list(slc)
        slclist[axis] = slice(*tup)
        slices[idx] = tuple(slclist)
    return slices


def reduce_paths_flexible(paths: Iterable[str],
                          dimension_tag: Union[str, tuple, list],
                          replace_with: str = 'set') -> str:
    """
    Reduces a list of similar paths by merging over the specified dimension.

    - If `dimension_tag` is a string (e.g., 'T' or 'Channel'), it's assumed to be followed by digits;
      the digits are replaced with `replace_with`.
    - If `dimension_tag` is a tuple/list (e.g., ('blue', 'red')), those are treated as categorical tokens
      and replaced with their joined value plus `replace_with`.
    """
    paths = list(paths)
    if not paths:
        return ""

    if isinstance(dimension_tag, str):
        # Match like 'T0001', 'Channel2', etc.
        pattern = re.compile(rf'({re.escape(dimension_tag)})(\d+)')
        def replace_tag(path):
            return pattern.sub(lambda m: m.group(1) + replace_with, path)

    elif isinstance(dimension_tag, (tuple, list)):
        # Categorical case: match only if surrounded by boundaries like /, _, -, ., or start/end of string
        unique_vals = sorted(set(dimension_tag))
        joined_val = ''.join(unique_vals) + replace_with

        # Example: match (^|/|_|-|.)blue(?=$|/|_|-|.)
        pattern = re.compile(
            rf'(?:(?<=^)|(?<=[/_\-.]))({"|".join(map(re.escape, unique_vals))})(?=$|[\/_\-.])'
        )

        def replace_tag(path):
            return pattern.sub(joined_val, path)

    else:
        raise ValueError("dimension_tag must be a string or a tuple/list of strings")

    # Apply replacement
    replaced_paths = [replace_tag(p) for p in paths]

    # Now combine all paths token-wise
    tokenized = [re.split(r'([/_\-.])', p) for p in replaced_paths]
    merged_tokens = []
    for tokens in zip(*tokenized):
        uniq = list(dict.fromkeys(tokens))  # preserve order
        merged_tokens.append(''.join(uniq))

    return ''.join(merged_tokens)


class FileSet:  # TODO: add a pixel_size parameter
    """
    Make sure the filepaths are sorted before passing them to this class.
    This class also assumes that the input files can contain maximum 5 dimensions.
    """

    """
    A class to manage file paths and their shapes.

    This class takes the file paths and their shapes as input and stores them in a dictionary.
    The shapes are used to determine the size of the arrays.
    The dimension tags are used to determine the axes of the arrays.
    The specified axes are the axes that are used to create slices.
    The slice dict is used to store the slices of the arrays.
    The path dict is used to store the paths of the arrays.
    """

    def __init__(self,
                 filepaths: Iterable[str],
                 shapes: Iterable[tuple | list] = None,
                 axis_tag0: Union[str, tuple] = None,
                 axis_tag1: Union[str, tuple] = None,
                 axis_tag2: Union[str, tuple] = None,
                 axis_tag3: Union[str, tuple] = None,
                 axis_tag4: Union[str, tuple] = None,
                 arrays: Iterable[da.Array] = None
                 # pixel_sizes: Iterable = None # TODO
                 ):
        """
        Initialize the FileSet class.

        Args:
            filepaths (Iterable[str]): The file paths of the arrays.
            shapes (Iterable[tuple | list], optional): The shapes of the arrays. Defaults to None.
            axis_tag0 (Union[str, tuple], optional): The tag of the axis. Defaults to None.
            axis_tag1 (Union[str, tuple], optional): The tag of the axis. Defaults to None.
            axis_tag2 (Union[str, tuple], optional): The tag of the axis. Defaults to None.
            axis_tag3 (Union[str, tuple], optional): The tag of the axis. Defaults to None.
            axis_tag4 (Union[str, tuple], optional): The tag of the axis. Defaults to None.
            arrays (Iterable[da.Array], optional): The arrays. Defaults to None.
        """
        assert shapes is not None or arrays is not None, f"Either shapes or arrays must be supplied."
        self.axis_dict = {
                0: 't',
                1: 'c',
                2: 'z',
                3: 'y',
                4: 'x'
        }
        if arrays is not None:
            self.array_dict = dict(zip(filepaths, arrays))
            shapes = [arr.shape for arr in arrays]
        else:
            self.array_dict = None

        self.region_dict = {path: arr.copy() for path, arr in self.array_dict.items()}

        self.shape_dict = dict(zip(filepaths, shapes))
        # self.axis_tag0 = axis_tag0
        # self.axis_tag1 = axis_tag1
        # self.axis_tag2 = axis_tag2
        # self.axis_tag3 = axis_tag3
        # self.axis_tag4 = axis_tag4
        # self.axis_tags = {
        #     0: axis_tag0,
        #     1: axis_tag1,
        #     2: axis_tag2,
        #     3: axis_tag3,
        #     4: axis_tag4
        # }
        full_axis_list = list(range(5))
        self.axis_tags = [axis_tag0, axis_tag1, axis_tag2, axis_tag3, axis_tag4]
        dimension_tags, specified_axes = [], []
        for axis, tag in zip(full_axis_list, self.axis_tags):
            if tag is not None:
                dimension_tags.append(tag)
                specified_axes.append(axis)

        self.dimension_tags = dimension_tags
        self.specified_axes = specified_axes

        self.group = {'': filepaths}
        assert len(self.dimension_tags) == len(self.specified_axes)
        self.slice_dict = {path: tuple(slice(0, size) for size in shape) for path, shape in self.shape_dict.items()}
        self.path_dict = dict(zip(filepaths, filepaths))

    # def detect_voxel_meta(self):
    #     self.vmeta = VoxelMetaReader(self._reference_filepath)
    # def _axis_as_str(self, axis: int):
    #     ax_dict = {0 : 't',
    #                1: 'c',
    #                2: 'z',
    #                3: 'y',
    #                4: 'x'
    #                }
    #     return ax_dict[axis]

    # def _get_concatenation_axis(self, dimension_tag):
    #     return self.specified_axes[self.dimension_tags.index(dimension_tag)]

    def get_numerics_per_dimension_tag(self,
                                       dimension_tag: str
                                       ) -> List[str]:
        """
        Extract numeric values from filepaths for a given dimension tag.

        Args:
            dimension_tag (str): The dimension tag to extract numerics for
                (e.g., 't' for time).

        Returns:
            list: List of numeric strings extracted from the filepaths.

        Example:
            >>> f = FileSet(['file_t0001_channel1.ome.tif', 'file_t0002_channel2.ome.tif'])
            >>> f.get_numerics_per_dimension_tag('t')
            ['0001', '0002']
        """
        filepaths = list(self.group.values())[0]
        matches = get_matches(f'{dimension_tag}\d+', filepaths)
        spans = [match.string[match.start():match.end()] for match in matches]
        numerics = [get_numerics(span)[0] for span in spans]
        # TODO: add an incrementality validator
        return numerics

    def _csplit_by(self, tup: tuple) -> dict:
        """
        Split the filepaths in the group by the given dimension tags.

        Args:
            tup (tuple): A tuple of dimension tags to split by.

        Returns:
            dict: The split group as a dictionary.
        """
        group = copy.deepcopy(self.group)
        for key, filepaths in group.items():
            # Initialize a dictionary to store the split filepaths
            alpha_dict = {key: [] for key in tup}
            for tag in tup:
                # Get matches for the current dimension tag
                matches = get_matches(f'{tag}', filepaths)
                # Extract the matched spans
                spans = [match.string[match.start():match.end()] for match in matches]
                # Extract the matched filepaths
                matched_paths = [match.string for match in matches]
                # Create a copy of the spans
                alpha = copy.deepcopy(spans)
                # Get the unique categories for the current dimension tag
                alpha_categories = np.unique(alpha).tolist()
                # Check that there is only one category
                assert len(alpha_categories) == 1, f"Number of categories is not 1: {alpha_categories}"
                # Get the category tag
                alpha_tag = alpha_categories[0]
                # Store the matched filepaths in the alpha dictionary
                alpha_dict[alpha_tag] = matched_paths
            # Update the group with the split filepaths
            group = alpha_dict
        return group

    def _split_by(self, *args):
        """
        Split the filepaths in the group by the given dimension tags.

        Args:
            *args (str): The dimension tags to split by.

        Returns:
            dict: The split group as a dictionary.
        """
        group = copy.deepcopy(self.group)
        for dim in args:
            if dim not in self.dimension_tags:
                raise ValueError(f"The dimension '{dim}' is not among the given dimension_tags.")
            # If the dimension tag is a tuple or list, split by all of them
            if isinstance(dim, (tuple, list)):
                group = self._csplit_by(dim)
            else:
                numeric_dict = {}
                for key, filepaths in group.items():
                    matches = get_matches(f'{dim}\d+', filepaths)
                    spans = [match.string[match.start():match.end()] for match in matches]
                    spans = [span.replace(dim, '') for span in spans]  ### remove search term from the spans
                    numerics = [get_numerics(span)[0] for span in spans]
                    numeric_categories = np.unique(numerics).tolist()
                    for idx, num in enumerate(numerics):
                        for i, category in enumerate(numeric_categories):
                            if num == category:
                                if key != '':
                                    tag_key = ''.join([key, '-', dim, num])
                                else:
                                    tag_key = ''.join([dim, num])
                                    # print(f"hey: {dim, num, tag_key}")
                                if not tag_key in numeric_dict:
                                    numeric_dict[tag_key] = []
                                numeric_dict[tag_key].append(filepaths[idx])
                group = numeric_dict
        return group

    def concatenate_along(self,
                          axis: int
                          ) -> dict:
        """
        Concatenates the arrays in the group along the specified axis.

        Args:
            axis (int): The axis to concatenate along.

        Returns:
            dict: The updated group with concatenated arrays.

        Raises:
            ValueError: If the axis is not among the given dimension tags.
        """
        ax_dict = self.axis_dict
        # dimension_tag = self.__getattribute__(f'axis_tag{axis}')
        dimension_tag = self.axis_tags[axis]
        if not dimension_tag in self.dimension_tags:
            raise ValueError(f"The dimension '{dimension_tag}' is not among the given dimension_tags.")
        # Split the group by all dimension tags except the one specified by the axis
        to_split = [item for item in self.dimension_tags if item != dimension_tag]
        group = self._split_by(*to_split)
        # Get the axis position in the specified axes
        axis = self.specified_axes[self.dimension_tags.index(dimension_tag)]
        for key, paths in group.items():
            # Sort the paths by their natural order
            sorted_paths = natsorted(paths)
            # Get the slices and shapes for each path
            group_slices = [self.slice_dict[path] for path in sorted_paths]
            group_shapes = [self.shape_dict[path] for path in sorted_paths]
            # Get the reduced paths (i.e., without the dimension tag)
            group_reduced_paths = [self.path_dict[path] for path in sorted_paths]

            # Accumulate the slices along the specified axis
            new_slices = accumulate_slices_along_axis(group_shapes, axis, group_slices)
            # Calculate the new shape of the concatenated array
            new_shape = concatenate_shapes_along_axis(group_shapes, axis)
            # Create a new path by adding '_{ax_dict[axis]}set' to the reduced paths
            p = reduce_paths_flexible(group_reduced_paths,
                                     dimension_tag,
                                     # group_reduced_paths,
                                     f'_{ax_dict[axis]}set'
                                    )
            new_reduced_paths = [p] * len(group_reduced_paths)
            # new_reduced_paths = reduce_paths(group_reduced_paths,
            #                                  dimension_tag,
            #                                  # group_reduced_paths,
            #                                  # f'_{ax_dict[axis]}set'
            #                                  )

            # If arrays are present, concatenate them
            if self.array_dict is not None:
                group_arrays = [self.array_dict[path] for path in sorted_paths]
                new_array = da.concatenate(group_arrays, axis=axis)

            # Update the slice, shape, and path dictionaries
            for path, slc, reduced_path in zip(sorted_paths, new_slices, new_reduced_paths):
                self.slice_dict[path] = slc
                self.shape_dict[path] = new_shape
                self.path_dict[path] = reduced_path
                if self.array_dict is not None:
                    self.array_dict[path] = new_array

        return group

    # def get_table(self):
    #     import pandas as pd
    #     df = pd.DataFrame({"path": self.path_dict,
    #                        "slice": self.slice_dict,
    #                        "shape": self.shape_dict})
    #     return df

    # @property
    # def table(self):
    #     try:
    #         return self.get_table()
    #     except:
    #         return None

    def get_concatenated_arrays(self):
        """
        Returns a dictionary of concatenated arrays.

        The keys of the dictionary are the same as the keys of the `path_dict`.
        The values of the dictionary are lists of two items: the first item is the
        file path, and the second item is the concatenated array.
        """
        # Get unique paths and their corresponding keys
        unique_paths = []
        unique_input_paths = []
        unique_ids = []
        for key, path in self.path_dict.items():
            if path not in unique_paths:
                unique_input_paths.append(key)
                unique_paths.append(path)
                unique_ids.append(key)

        # Get concatenated arrays
        unique_arrays = [self.array_dict[path] for path in unique_ids]
        # Return a dictionary of concatenated arrays
        return {key: [path, arr] for key, path, arr in zip(unique_input_paths, unique_paths, unique_arrays)}
