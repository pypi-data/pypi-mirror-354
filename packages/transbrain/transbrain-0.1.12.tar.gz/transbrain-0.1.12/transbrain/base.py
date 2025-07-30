import numpy as np
import pandas as pd
from scipy import ndimage
from nilearn import image
from transbrain.config import Config

def get_region_phenotypes(phenotype_nii_path: str,atlas_dict: dict,method: str = 'mean',resample: bool = True,label_column: str = 'Atlas Index',
    region_column: str = 'Anatomical Name') -> pd.DataFrame:

    """
    Calculate region-wise phenotype values using a specified brain atlas.

    This function extracts regional statistics (mean or sum) from a phenotype NIfTI image 
    based on a chosen human or mouse brain atlas. The phenotype image can be automatically 
    resampled to match the atlas resolution if needed.

    Parameters
    ----------
    phenotype_nii_path : str
        Path to the input phenotype NIfTI file. Should be in MNI space for human atlases,
        or Allen CCFv3 space for mouse atlas.
    atlas_dict : dict
        A dictionary containing the following keys:
        - 'atlas': The loaded Mouse atlas image.
        - 'atlas_data': The atlas data as a numpy array.
        - 'region_info': A list of anatomical names for the specified regions.
        - 'info_table': The full ROI information table.

    method : {'mean', 'sum'}, optional
        Method for aggregating voxel values within each region. Default is 'mean'.
    resample : bool, optional
        If True, resample the atlas to match the shape and resolution of the phenotype image.
        Default is True.
    label_column : str, optional
        Name of the column in the atlas label CSV that contains numeric label indices.
        Default is 'Atlas Index'.
    region_column : str, optional
        Name of the column in the atlas label CSV that contains region names.
        Default is 'Anatomical Name'.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with aggregated phenotype values (mean or sum) for each region, , indexed by brain region name.
    """

    if method not in ('mean', 'sum'):
        raise ValueError(f"Invalid method: '{method}'. Use 'mean' or 'sum'")
    
    atlas_path = atlas_dict['atlas']
    atlas_df = atlas_dict['info_table']
    labels = atlas_df[label_column].values

    phenotype_img = image.load_img(phenotype_nii_path)
    atlas_img = image.load_img(atlas_path)

    if resample and phenotype_img.shape != atlas_img.shape:
        print("Resampling to match atlas...")
        atlas_img = image.resample_to_img(atlas_img, phenotype_img, interpolation='nearest')

    phenotype_arr = np.asarray(phenotype_img.dataobj)
    atlas_arr = np.asarray(atlas_img.dataobj)

    if phenotype_arr.shape != atlas_arr.shape:
        raise ValueError("Phenotype and atlas shape mismatch after resampling")
    
    if method == 'mean':
        region_values = ndimage.mean(phenotype_arr, labels=atlas_arr, index=labels)
    else: 
        region_values = ndimage.sum(phenotype_arr, labels=atlas_arr, index=labels)
    
    result_df = atlas_df.copy()
    result_df['Phenotype'] = region_values

    result_df = result_df[[region_column,'Phenotype']]
    result_df.columns = ['Region name','Phenotype']
    result_df = result_df.set_index('Region name')

    return result_df


