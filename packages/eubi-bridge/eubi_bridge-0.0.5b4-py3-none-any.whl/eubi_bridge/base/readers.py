import fsspec
import fsspec.core
import fsspec.compression
import fsspec.spec

from dask import delayed
import dask
from eubi_bridge.ngff.multiscales import Pyramid

readable_formats = ('.ome.tiff', '.ome.tif', '.czi', '.lif',
                    '.nd2', '.tif', '.tiff', '.lsm',
                    '.png', '.jpg', '.jpeg')

@delayed
def read_single_image_asarray(input_path, **kwargs):
    """
    Reads a single image file with Dask and returns the array.

    Parameters
    ----------
    input_path : str
        Path to the image file.
    **kwargs : dict
        Additional keyword arguments, such as `verbose` and `scene`.

    Returns
    -------
    arr : dask.array.Array
        The image array.
    """
    reader_kwargs = {}
    if input_path.endswith('.zarr'):
        input_path = f"/home/oezdemir/PycharmProjects/TIM2025/data/example_images/pff2zarr1/slice__zset.zarr"
        reader = Pyramid().from_ngff
    elif input_path.endswith(('ome.tiff', 'ome.tif')):
        from bioio_ome_tiff.reader import Reader as reader # pip install bioio-ome-tiff --no-deps
    elif input_path.endswith(('.tif', '.tiff', '.lsm')):
        from bioio_tifffile.reader import Reader as reader # pip install bioio-tifffile --no-deps
        reader_kwargs['chunk_dims'] = 'YX'
    elif input_path.endswith('.czi'):
        from bioio_czi.reader import Reader as reader
    elif input_path.endswith('.lif'):
        from bioio_lif.reader import Reader as reader
    elif input_path.endswith('.nd2'):
        from bioio_nd2.reader import Reader as reader
    elif input_path.endswith(('.png','.jpg','.jpeg')):
        from bioio_imageio.reader import Reader as reader
    else:
        from bioio_bioformats.reader import Reader as reader
    verbose = kwargs.get('verbose', False)
    if verbose:
        print(f"Reading with {reader.__qualname__}.")
    im = reader(input_path, **reader_kwargs)
    if hasattr(im, 'set_scene'):
        im.set_scene(kwargs.get('scene', 0))
        arr = im.get_image_dask_data('TCZYX')
    elif hasattr(im, 'base_array'):
        arr = im.base_array
    else:
        raise Exception(f"Unknown reader: {reader.__qualname__}")
    if arr.ndim > 5:
        arr = arr[0].transpose((0, 4, 1, 2, 3))
    return arr

def get_metadata_reader_by_path(input_path, **kwargs):
    # if path.endswith(':
    #     return importlib.import_module('bfio').BioReader,
    # if path.endswith('czi'):
    #     return importlib.import_module('bioio_czi.reader').Reader
    # elif path.endswith('lif'):
    #     return importlib.import_module('bioio_lif.reader').Reader
    # else:
    #     return importlib.import_module('bioio_bioformats.reader').Reader
    if input_path.endswith(('ome.tiff', 'ome.tif')):
        from bioio_ome_tiff.reader import Reader as reader # pip install bioio-ome-tiff --no-deps
    elif input_path.endswith(('.tif', '.tiff', '.lsm')):
        from bioio_tifffile.reader import Reader as reader
    elif input_path.endswith('.czi'):
        from bioio_czi.reader import Reader as reader
    elif input_path.endswith('.lif'):
        from bioio_lif.reader import Reader as reader
    elif input_path.endswith('.nd2'):
        from bioio_nd2.reader import Reader as reader
    elif input_path.endswith(('.png','.jpg','.jpeg')):
        from bioio_imageio.reader import Reader as reader
    else:
        from bioio_bioformats.reader import Reader as reader
    return reader

def read_metadata_via_bioio_bioformats(input_path, **kwargs):
    from bioio_bioformats.reader import Reader
    series = kwargs.get('series', None)
    img = Reader(input_path)
    if series is not None:
        img.set_scene(series)
    omemeta = img.ome_metadata
    return omemeta

def read_metadata_via_bfio(input_path, **kwargs):
    from bfio import BioReader
    omemeta = BioReader(input_path, backend='bioformats').metadata
    return omemeta

def read_metadata_via_extension(input_path, **kwargs):
    Reader = get_metadata_reader_by_path(input_path)
    series = kwargs.get('series', None)
    img = Reader(input_path)
    if series is not None:
        img.set_scene(series)
    omemeta = img.ome_metadata
    return omemeta

# import glob
#
# imgs = glob.glob(f"/home/oezdemir/PycharmProjects/TIM2025/data/example_images/pff/*", recursive = True)
# arrs = [read_single_image_asarray(img, verbose = True) for img in imgs]
# arrs = dask.compute(*arrs)
# for arr in arrs:
#     arr_ = arr.compute()
#     print(arr_.shape)


# from bioio_nd2.reader import Reader as reader
# r = reader('/home/oezdemir/PycharmProjects/TIM2025/data/example_images/pff/190821_L1_IRS-Akt_CS2003.nd2')
# scene_name = r.scenes[0]
# r.set_scene(scene_name)
# arr = r.get_image_dask_data('TCZYX')

#
# input_path = f'/home/oezdemir/PycharmProjects/nextflow_convert/test/MVI_1349-00017.jpg'
#
# arrs = [read_single_image_asarray(input_path, verbose = True)]
# arr_ = dask.compute(*arrs)

# from bioio_ome_tiff.reader import Reader as reader
# r = reader('/home/oezdemir/PycharmProjects/TIM2025/data/example_images/pff/tubhiswt_C0_TP0.ome.tif')
# scene_name = r.scenes[0]
# r.set_scene(scene_name)
# arr = r.get_image_dask_data('TCZYX')

# input_path = f"/home/oezdemir/PycharmProjects/TIM2025/data/example_images/tubhiswt-4D/tubhiswt_C0_TP0.ome.tif"
# arrs = [read_single_image_asarray(input_path, verbose = True)]
# arr_ = dask.compute(*arrs)

# input_path = f"/home/oezdemir/PycharmProjects/TIM2025/data/example_images/pff2zarr1.zarr"
# arrs = [read_single_image_asarray(input_path, verbose = True)]
# arr_ = dask.compute(*arrs)

