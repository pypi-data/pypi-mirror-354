import numpy as np
import statistics


# ******************************************************************************************************************************************************************
## List of modules in 'kbomodels' Python package. 
# ******************************************************************************************************************************************************************
def modules_list():
    print("""
    Kabirian-Based Optinalysis Models

    Kabirian-based optinalysis models (*kbomodels*) consist of a collection of mathematical and statistical techniques designed for analyzing datasets within the 
    Kabirian-based optinalysis framework, along with other advanced methodologies. The estimation modules integrated within kbomodels include:

    1a. kc_isoptinalysis : Performs Kabirian-based isomorphic optinalysis to calculate the Kabirian coefficient.
    1b. doc_kc_isoptinalysis : Prints the documentation of the kc_isoptinalysis module. 

    2a. kc_autoptinalysis : Performs Kabirian-based automorphic optinalysis to calculate the Kabirian coefficient.
    2b. doc_kc_autoptinalysis : Prints the documentation of the kc_autoptinalysis.

    3a. pSimSymId : Translates the Kabirian coefficient of similarity, symmetry, or identity (kc) to probability of similarity, symmetry, or Sidentity (SimSymId).
    3b. doc_pSimSymId : Prints the documentation of the pSimSymId.
        
    4a. pDsimAsymUid : Translates probability of similarity, symmetry, or identity (pSimSymId) to probability of dissimilarity, asymmetry, or unidentity (pDsimAsymUid).
    4b. doc_pDsimAsymUid : Prints the documentation of the pDsimAsymUid.
        
    5a. kc_alt1 : Translates probability of similarity, symmetry, or identity (pSimSymId) to an ascending-alternative (A-alternative) Kabirian coefficient of similarity, symmetry, or identity (kc_alt1).
    5b. doc_kc_alt1 : Prints the documentation of the kc_alt1.
        
    6a. kc_alt2 : Translates probability of similarity, symmetry, or identity (pSimSymId) to a descending-alternative (D-alternative) Kabirian coefficient of similarity, symmetry, or identity (kc_alt2).
    6b. doc_kc_alt2 : Prints the documentation of the kc_alt2.
        
    7a. kc_alt : Translates Kabirian coefficient of similarity, symmetry, or identity (kc) to its inverse alternative Kabirian coefficient of similarity, symmetry, or identity (kc_alt).
    7b. doc_kc_alt : Prints the documentation of the kc_alt.
        
    8a. isomorphic_optinalysis : Performs Kabirian-based isomorphic optinalysis.
    8b. doc_isomorphic_optinalysis : Prints the documentation of the isomorphic_optinalysis.

    9a. automorphic_optinalysis : Performs Kabirian-based automorphic optinalysis.
    9b. doc_automorphic_optinalysis : Prints the documentation of the automorphic_optinalysis.

    10a. stat_SymAsymmetry : Estimates the statistical symmetry and asymmetry of a dataset using a customized, and optimized Kabirian-based automorphic optinalysis.
    10b. doc_stat_SymAsymmetry : Prints the documentation of the stat_SymAsymmetry.
        
    11a. bioseq_gpa : Perform pairwise sequence analysis of aligned biological sequences using a customized, and optimized Kabirian-based    isomorphic optinalysis. 
    11b. doc_bioseq_gpa : Prints the documentation of the bioseq_gpa.
        
    12a. stat_mirroring : Performs statistical dispersion estimations on a dataset using a parameterized, customized, and optimized Kabirian-based isomorphic optinalysis.
    12b. doc_stat_mirroring : Prints the documentation of the stat_mirroring.
        
    13a. famispacing : Estimates family spacing conformity and disconformity using a customized, and optimized Kabirian-based isomorphic optinalysis.
    13b. doc_famispacing : Prints the documentation of the famispacing.
        
    14a. smb_ordinalysis : Perform statistical mirroring-based ordinalysis (SM-based Ordinalysis), a methodology for assessing an individual's level of assessments on a defined ordinal scale by applying a customized and optimized statistical mirroring techniques.
    14b. doc_smb_ordinalysis : Prints the documentation of the smb_ordinalysis. 
    
    15a. qualitative_exposuremetrics : Perform qualitative exposuremetrics analysis, a methodology for analyzing organismal resistance and susceptibility dynamics using qualitative variables.
    15b. doc_qualitative_exposuremetrics : Prints the documentation of the qualitative_exposuremetrics. 

    """) 



# ******************************************************************************************************************************************************************
## Function for computing Kabirian coefficient (kc) during isomorphic optinalysis
# ******************************************************************************************************************************************************************
def kc_isoptinalysis(instruction_list: list) -> float:
    """
    Performs Kabirian-based isomorphic optinalysis to calculate the Kabirian coefficient.

    Args:
        instruction_list (list): A list of parameters, including:
            - data_x (list): First dataset (a list of numerical values).
            - data_y (list): Second dataset (a list of numerical values).
            - pairing (str): Specifies the type of pairing to use. Valid options are:
                * "pairing:H_H" or "H_H"    - For head-to-head pairing (the lowest ends of the isoreflective pair of points are maximally distant). 
                * "pairing:T_T" or "T_T"    - For tail-to-tail pairing (the lowest ends of the isoreflective pair of points are minimally distant).

    Returns:
        float - The calculated kc_optinalysis coefficient, which quantifies the isomorphic 
        relationship between the two datasets based on the provided pairing type.

    Raises:
        ValueError: If the provided pairing type is invalid (i.e., not "H_H" or "T_T").

    Example:
        >>> import kbomodels as kbo
        >>> data_x = [1, 0, 2, 4.25]
        >>> data_y = [0, 5.47, 2.10, 90]
        >>> instruction_list = [data_x, data_y, "pairing:H_H"]
        >>> kbo.kc_isoptinalysis(instruction_list)
        0.8419818140924717

        >>> instruction_list = [data_x, data_y, "pairing:T_T"]
        >>> kbo.kc_isoptinalysis(instruction_list)
        0.5973738801376889
    
    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Extracting data from the instruction_list
    data_x = instruction_list[0]
    data_y = instruction_list[1]
    pairing = instruction_list[2]
        
    # Generating a list of optiscale values from 0.01 to 2 times the length of data_x
    optiscale = [p / 100 for p in range(1, (2 * len(data_x) + 2))]

    # Calculating the mid-point of the optiscale values
    mid_optiscale = (optiscale[0] * len(data_x)) + optiscale[0]

    # setting a normalization_value
    normalization_value = 0

    # Generating the isoreflective list based on the pairing type
    if pairing == "pairing:H_H" or pairing == "H_H":
            isoreflective_list = data_x + [normalization_value] + (data_y[::-1])  
    elif pairing == "pairing:T_T" or pairing == "T_T":
            isoreflective_list = (data_x[::-1]) + [normalization_value] + data_y
    else:
        raise ValueError('Invalid pairing command. Use "pairing:H_H" or "H_H", "pairing:T_T" or "T_T" ')

    # Calculating the dot product of isoreflective_list and optiscale
    sum_of_scalements = np.dot(isoreflective_list, optiscale)

    # Calculating the kc_optinalysis using the calculated values
    kc_optinalysis = (mid_optiscale * sum(isoreflective_list)) / sum_of_scalements

    # Returning the calculated kc_optinalysis value
    return float(kc_optinalysis)


def doc_kc_isoptinalysis():
    print("""
    Performs Kabirian-based isomorphic optinalysis to calculate the Kabirian coefficient.

    Args:
        instruction_list (list): A list of parameters, including:
            - data_x (list): First dataset (a list of numerical values).
            - data_y (list): Second dataset (a list of numerical values).
            - pairing (str): Specifies the type of pairing to use. Valid options are:
                * "pairing:H_H" or "H_H"    - For head-to-head pairing (the lowest ends of the isoreflective pair of points are maximally distant). 
                * "pairing:T_T" or "T_T"    - For tail-to-tail pairing (the lowest ends of the isoreflective pair of points are minimally distant).

    Returns:
        float - The calculated kc_optinalysis coefficient, which quantifies the isomorphic 
        relationship between the two datasets based on the provided pairing type.

    Raises:
        ValueError: If the provided pairing type is invalid (i.e., not "H_H" or "T_T").

    Example:
        >>> import kbomodels as kbo
        >>> data_x = [1, 0, 2, 4.25]
        >>> data_y = [0, 5.47, 2.10, 90]
        >>> instruction_list = [data_x, data_y, "pairing:H_H"]
        >>> kbo.kc_isoptinalysis(instruction_list)
        0.8419818140924717

        >>> instruction_list = [data_x, data_y, "pairing:T_T"]
        >>> kbo.kc_isoptinalysis(instruction_list)
        0.5973738801376889
    
    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)



# *****************************************************************************************************************************************************************
## Function for computing Kabirian coefficient (kc) during automorphic 
# ******************************************************************************************************************************************************************
def kc_autoptinalysis(data: list) -> float:
    """
    Performs Kabirian-based automorphic optinalysis to calculate the Kabirian coefficient.

    Args:
        data (list) :
            A list of numerical values.

    Returns:
        float - The calculated Kabirian coefficient (kc), which measures symmetry coefficient in the data.

    Raises:
        ValueError: None

    Examples:
        >>> import kbomodels as kbo
        >>> data = [1, 2, 3, 4, 5, 6, 9, 6, 5, 4, 3, 2, 1]
        >>> kbo.kc_autoptinalysis(data)
        1.0000000

        >>> data = [2, 5, 9, 1, 3, 2, 0, 2, 3, 1, 9, 5, 2]
        >>> kbo.kc_autoptinalysis(data)
        1.0000000

    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Generate a list of optiscale values from 0.01 to the length of data
    optiscale = [p / 100 for p in range(1, len(data) + 1)]

    # Calculate the mid_optiscale value
    mid_optiscale = ((optiscale[0] * len(data)) + optiscale[0]) / 2

    # Create an autoreflective list using the input data
    autoreflective_list = data

    # Calculate the dot product of autoreflective_list and optiscale
    sum_of_scalements = np.dot(autoreflective_list, optiscale)

    # Calculate the kc_optinalysis using the computed values
    kc_optinalysis = (mid_optiscale * sum(autoreflective_list)) / sum_of_scalements

    return float(kc_optinalysis)


def doc_kc_autoptinalysis():
    print("""
    Performs Kabirian-based automorphic optinalysis to calculate the Kabirian coefficient.

    Args:
        data (list) :
            A list of numerical values.

    Returns:
        float - The calculated Kabirian coefficient (kc), which measures symmetry coefficient in the data.

    Raises:
        ValueError: None

    Examples:
        >>> import kbomodels as kbo
        >>> data = [1, 2, 3, 4, 5, 6, 9, 6, 5, 4, 3, 2, 1]
        >>> kbo.kc_autoptinalysis(data)
        1.0000000

        >>> data = [2, 5, 9, 1, 3, 2, 0, 2, 3, 1, 9, 5, 2]
        >>> kbo.kc_autoptinalysis(data)
        1.0000000

    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3)  
    """)



# ******************************************************************************************************************************************************************
## Function for translating Kabirian coefficient of similarity, symmetry, or identity (kc) to probability of similarity, symmetry, or identity (SimSymId).
# ******************************************************************************************************************************************************************
def pSimSymId(kc, num_of_dimensions) -> float:
    """
    Translates the Kabirian coefficient of similarity, symmetry, or identity (kc) to probability of similarity, symmetry, or identity (SimSymId).

    **Args:**
        The two input parameters:
            * kc (float): The Kabirian coefficient of similarity, symmetry, or identity, which can be within or outside the range [0, 1].
            * num_of_dimensions (int): The number of dimensions (sample size) involved in the analysis.

    **Returns:**
        float - The calculated probability of similarity, symmetry, or identity (pSimSymId).

    **Raises:**
        ValueError: None

    **Examples:**
        >>> import kbomodels as kbo
        >>> kbo.pSimSymId(0.515385, 3)
        -0.11258202125629384

        >>> kbo.pSimSymId(1.232452, 3)
        0.5981089064489609

    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Check if kc is within the valid range [0, 1]
    if 0 <= kc <= 1:
        # Calculate pSimSymId using the formula for kc in [0, 1]
        SimSymId = ((num_of_dimensions + 1) - kc * ((2 * num_of_dimensions) + 1)) / (kc - (num_of_dimensions + 1))
    else:
        # Calculate pSimSymId using the formula for kc outside the range [0, 1]
        SimSymId = ((num_of_dimensions + 1) - kc) / (kc * ((2 * num_of_dimensions) + 1) - (num_of_dimensions + 1))
    
    return float(SimSymId)  # Return the calculated SimSymId value


def doc_pSimSymId():
    print("""
    Translates the Kabirian coefficient of similarity, symmetry, or identity (kc) to probability of similarity, symmetry, or identity (SimSymId).

    Args:
        The two input parameters:
            * kc (float): The Kabirian coefficient of similarity, symmetry, or identity, which can be within or outside the range [0, 1].
            * num_of_dimensions (int): The number of dimensions (sample size) involved in the analysis.

    Returns:
        float - The calculated probability of similarity, symmetry, or identity (pSimSymId).

    Raises:
        ValueError: None

    Examples:
        >>> import kbomodels as kbo
        >>> kbo.pSimSymId(0.515385, 3)
        -0.11258202125629384

        >>> kbo.pSimSymId(1.232452, 3)
        0.5981089064489609

    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)
    return



# *****************************************************************************************************************************************************************
## Function for translating probability of similarity, symmetry, or identity (pSimSymId) to probability of dissimilarity, asymmetry, or unidentity (pDsimAsymUid)
# ******************************************************************************************************************************************************************
def pDsimAsymUid(SimSymId) -> float:
    """
    Translates probability of similarity, symmetry, or identity (pSimSymId) to probability of dissimilarity, asymmetry, or unidentity (pDsimAsymUid).

    **Args:**
        The input parameter:
            * pSimSymId (float): The probability of similarity, symmetry, or identity, which can be within the range [-1, 1].

    **Returns:**
        float - The calculated probability of dissimilarity, asymmetry, or unidentity (pDsimAsymUid).

    **Raises:**
        ValueError: None

    **Examples:**
        >>> import kbomodels as kbo
        >>> kbo.pDsimAsymUid(-0.11258202125629384)
        -0.8874179787437062

        >>> kbo.pDsimAsymUid(0.5981089064489609)
        0.40189109355103914
    
    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Check if pSimSymId is within the valid range [0, 1]
    if 0 <= SimSymId <= 1:
        # Calculate pDsimAsymUid when pSimSymId is in [0, 1]
        DsimAsymUid = 1 - SimSymId
    else:
        # Calculate pDsimAsymUid when pSimSymId is outside [0, 1]
        DsimAsymUid = -1 - SimSymId
    
    return float(DsimAsymUid)


def doc_pDsimAsymUid():
    print("""
    Translates probability of similarity, symmetry, or identity (pSimSymId) to probability of dissimilarity, asymmetry, or unidentity (pDsimAsymUid).

    Args:
        The input parameter:
            * pSimSymId (float): The probability of similarity, symmetry, or identity, which can be within the range [-1, 1].

    Returns:
        float - The calculated probability of dissimilarity, asymmetry, or unidentity (pDsimAsymUid).

    Raises:
        ValueError: None

    Examples:
        >>> import kbomodels as kbo
        >>> kbo.pDsimAsymUid(-0.11258202125629384)
        -0.8874179787437062

        >>> kbo.pDsimAsymUid(0.5981089064489609)
        0.40189109355103914
    
    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)



# *****************************************************************************************************************************************************************
## Function for translating Kabirian coefficient of similarity, symmetry, or identity (kc) to its inverse alternative Kabirian coefficient of similarity, symmetry, or identity (kcalt)
# ******************************************************************************************************************************************************************
def kc_alt(kc, pSimSymId, num_of_dimensions) -> float:
    """
    Translates Kabirian coefficient of similarity, symmetry, or identity (kc) to its inverse alternative Kabirian coefficient of similarity, symmetry, or identity (kc_alt).

    **Args:**
        The three input parameters:
            * kc (float): The original Kabirian coefficient, which can be within or outside the range [0, 1].
            * pSimSymId (float): The probability of similarity, symmetry, or identity value.
            * num_of_dimensions (int): The number of dimensions (sample size) involved in the analysis.

    **Returns:**
        float - The calculated alternative Kabirian coefficient (kc_alt).

    **Raises:**
        ValueError: None

    **Examples:**
        >>> import kbomodels as kbo
        >>> kbo.kc_alt(0.515385, -0.1126, 3)
        16.759206798866856

        >>> kbo.kc_alt(1.232452, 0.5981, 3)
        0.8413155920559088

    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    if 0 <= kc <= 1:
        # Calculate kc_alt when kc is in [0, 1]
        kc_alt = ((num_of_dimensions + 1) * (pSimSymId + 1)) / (((2 * num_of_dimensions) + 1) * pSimSymId + 1)
    else:
        # Calculate kc_alt when kc is outside [0, 1]
        kc_alt = ((num_of_dimensions + 1) * (pSimSymId + 1)) / (pSimSymId + ((2 * num_of_dimensions) + 1))
    
    return float(kc_alt)


def doc_kc_alt():
    print("""
    Translates Kabirian coefficient of similarity, symmetry, or identity (kc) to its inverse alternative Kabirian coefficient of similarity, symmetry, or identity (kc_alt).

    Args:
        The three input parameters:
            * kc (float): The original Kabirian coefficient, which can be within or outside the range [0, 1].
            * pSimSymId (float): The probability of similarity, symmetry, or identity value.
            * num_of_dimensions (int): The number of dimensions (sample size) involved in the analysis.

    Returns:
        float - The calculated alternative Kabirian coefficient (kc_alt).

    Raises:
        ValueError: None

    Examples:
        >>> import kbomodels as kbo
        >>> kbo.kc_alt(0.515385, -0.1126, 3)
        16.759206798866856

        >>> kbo.kc_alt(1.232452, 0.5981, 3)
        0.8413155920559088

    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)



# *****************************************************************************************************************************************************************
## Function for translating probability of similarity, symmetry, or identity (pSimSymId) to an ascending-alternative (A-alternative) Kabirian coefficient of similarity, symmetry, or identity (kcalt1)
# ******************************************************************************************************************************************************************
def kc_alt1(pSimSymId, num_of_dimensions) -> float:
    """
    Translates probability of similarity, symmetry, or identity (pSimSymId) to an ascending-alternative (A-alternative) Kabirian coefficient of similarity, symmetry, or identity (kc_alt1).

    **Args:**
        The two input parameters:
            * pSimSymId (float): The probability of similarity, symmetry, or identity value.
            * num_of_dimensions (int): The number of dimensions (sample size) involved in the analysis.

    **Returns:**
        float - The calculated A-alternative Kabirian coefficient (kc_alt1).

    **Raises:**
        ValueError: None

    **Examples:**S
        >>> import kbomodels as kbo
        >>> kbo.kc_alt1(0.5981, 3)
        0.8413155920559088

        >>> kbo.kc_alt1(0.5981, 25)
        0.8052738376025474

    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Calculate kc_alt1
    kc_alt1 = ((num_of_dimensions + 1) * (pSimSymId + 1)) / (pSimSymId + ((2 * num_of_dimensions) + 1))
    
    return float(kc_alt1)


def doc_kc_alt1():
    print("""
    Translates probability of similarity, symmetry, or identity (pSimSymId) to an ascending-alternative (A-alternative) Kabirian coefficient of similarity, symmetry, or identity (kc_alt1).

    Args:
        The two input parameters:
            * pSimSymId (float): The probability of similarity, symmetry, or identity value.
            * num_of_dimensions (int): The number of dimensions (sample size) involved in the analysis.

    Returns:
        float - The calculated A-alternative Kabirian coefficient (kc_alt1).

    Raises:
        ValueError: None

    Examples:
        >>> import kbomodels as kbo
        >>> kbo.kc_alt1(0.5981, 3)
        0.8413155920559088

        >>> kbo.kc_alt1(0.5981, 25)
        0.8052738376025474

    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2023). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)



# *****************************************************************************************************************************************************************
## Function for translating probability of similarity, symmetry, or identity (pSimSymId) to descending-alternative (D-alternative) Kabirian coefficient of similarity, symmetry, or identity (kcalt2)
# ******************************************************************************************************************************************************************
def kc_alt2(pSimSymId, num_of_dimensions) -> float:
    """
    Translates probability of similarity, symmetry, or identity (pSimSymId) to a descending-alternative (D-alternative) Kabirian coefficient of similarity, symmetry, or identity (kc_alt2).

    **Args:**
        The two input parameters :
            * pSimSymId (float): The probability of similarity, symmetry, or identity value.
            * num_of_dimensions (int): The number of dimensions (sample size) involved in the analysis.

    **Returns:**
        float - The calculated alternative Kabirian coefficient (kc_alt2).

    **Raises:**
        ValueError: None

    **Examples:**
        >>> import kbomodels as kbo
        >>> kbo.kc_alt2(0.5981, 3)
        1.2324599456301695

        >>> kbo.kc_alt2(0.5981, 25)
        1.3189368665305956

    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Calculate kc_alt2
    kc_alt2 = ((num_of_dimensions + 1) * (pSimSymId + 1)) / (((2 * num_of_dimensions) + 1) * pSimSymId + 1)
    
    return float(kc_alt2)


def doc_kc_alt2():
    print("""
    Translates probability of similarity, symmetry, or identity (pSimSymId) to a descending-alternative (D-alternative) Kabirian coefficient of similarity, symmetry, or identity (kc_alt2).

    Args:
        The two input parameters :
            * pSimSymId (float): The probability of similarity, symmetry, or identity value.
            * num_of_dimensions (int): The number of dimensions (sample size) involved in the analysis.

    Returns:
        float - The calculated alternative Kabirian coefficient (kc_alt2).

    Raises:
        ValueError: None

    Examples:
        >>> import kbomodels as kbo
        >>> kbo.kc_alt2(0.5981, 3)
        1.2324599456301695

        >>> kbo.kc_alt2(0.5981, 25)
        1.3189368665305956

    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)



# *****************************************************************************************************************************************************************
## Function for performing isomorphic optinalysis
# ******************************************************************************************************************************************************************
def isomorphic_optinalysis(instruction_list: list) -> any:
    """
    Performs Kabirian-based isomorphic optinalysis.

    This function processes two datasets (data_x, data_y) and a pairing type to generate an isoreflective list. The pairing type determines the arrangement of the data, 
    and then the Kabirian coefficient of optinalyis is calculated based on the dot product of the isoreflective list (bijective isomorphism) and an optiscale. 
    The result is a single estimate of Kabirian coefficient (kc) of similarity (relationship) between the two datasets. The kc value is then translated into probalitities 
    and other alternate inverse or equivalent coefficients. The kc translations followed a systemetic Kabirian Y-rule of isomorphic optinalysis.    

    This function calculates several Kabirian-based isomorphic optinalysis estimates such as:
        - Kabirian coefficient of similarity (kc).
        - Probability of similarity (psim).
        - Probability of dissimilarity (pdsim).
        - Alternative Kabirian coefficients (kc_alt1, kc_alt2, kc_alt).
    
    Args:
        instruction_list (list): A list containing the following four elements:
            - data_x (list)   : First dataset for comparison.
            - data_y (list)   : Second dataset for comparison.
            - pairing (str)   : Specifies the pairing type. Options include: 
                * "pairing:H_H" or "H_H"    : For head-to-head (the lowest ends of the isoreflective pair of points are maximally distant).
                * "pairing:T_T" or "T_T"    : For tail-to-tail (the lowest ends of the isoreflective pair of points are minimally distant).
            - print_result (str) : Specifies the result to return. Options include:
                * "print:kc" or "kc"         : Prints the Kabirian coefficient of similarity.
                * "print:psim" or "psim"     : Prints the probability of similarity.
                * "print:pdsim" or "pdsim"   : Prints the probability of dissimilarity.
                * "print:kcalt1" or "kcalt1" : Prints the A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2" : Prints the D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"   : Prints the the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If an invalid pairing type or `print_result` option is provided.

    Examples:
        >>> import kbomodels as kbo
        >>> instruction_list = [[1, 0, 2, 4.25], [0, 5.47, 2.10, 90], "pairing:H_H", "print:kc"]
        >>> kbo.isomorphic_optinalysis(instruction_list)
        0.8419818140924717

        >>> instruction_list = [[1, 0, 2, 4.25], [0, 5.47, 2.10, 90], "pairing:T_T", "print:all_in_list"]
        >>> kc, psim, pdsim, kc_alt1, kc_alt2, kc_alt = kbo.isomorphic_optinalysis(instruction_list)
        >>> kc, psim, pdsim, kc_alt1, kc_alt2, kc_alt
        (0.5973738801376889, 0.08548645989747836, 0.9145135401025216, 0.5973738801376889, 3.0674236216785666, 3.0674236216785666)

    **Process:**
        1. The function first extracts data_x, data_y, and pairing type from the instruction_list.
        2. It generates an optiscale, which is a list of values from 0.01 to 2 times the length of data_x.
        3. Based on the pairing type ("H_H" or "T_T"), it creates an isoreflective list by combining data_x and data_y with a zero separator.
        4. Calculates the Kabirian coefficient (kc) through the `kc_isoptinalysis` function, which computes kc based on an isoreflective process of the data.
        5. Determines the number of dimensions (sample size) from the data.
        6. Selects the requested output based on `print_result` and computes the other additional estimates such as:
            * `psim`    : Probability of similarity, calculated from kc.
            * `pdsim`   : Probability of dissimilarity, calculated from psim.
            * `kc_alt1`, `kc_alt2`, and `kc_alt` : Alternative Kabirian coefficients using different formulas.
        7. Finally returns the result.

    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """

    # Extracting input data from the instruction_list
    data_x = instruction_list[0]  
    data_y = instruction_list[1] 
    pairing = instruction_list[2]  
    print_result = instruction_list[3] 
    
    # Calculating the kc estimate of the isomorphic optinalysis
    kc = kc_isoptinalysis(instruction_list)
    num_of_dimensions = len(data_x)
    
    # Calculating (translating) other estimates of isomorphic optinalysis based on the selected result(s) to be printed from the print_result input
    if print_result == "print:kc" or print_result == "kc":
        result = kc
    elif print_result == "print:psim" or print_result == "psim":
        psim_value = pSimSymId(kc, num_of_dimensions)
        result = psim_value
    elif print_result == "print:pdsim" or print_result == "pdsim":
        psim_value = pSimSymId(kc, num_of_dimensions)
        pdsim_value = pDsimAsymUid(psim_value)
        result = pdsim_value
    elif print_result == "print:kcalt1" or print_result == "kcalt1":
        psim_value = pSimSymId(kc, num_of_dimensions)
        kc_alt1_value = kc_alt1(psim_value, num_of_dimensions)
        result = kc_alt1_value
    elif print_result == "print:kcalt2" or print_result == "kcalt2":
        psim_value = pSimSymId(kc, num_of_dimensions)
        kc_alt2_value = kc_alt2(psim_value, num_of_dimensions)
        result = kc_alt2_value
    elif print_result == "print:kcalt" or print_result == "kcalt":
        psim_value = pSimSymId(kc, num_of_dimensions)
        kc_alt_value = kc_alt(kc, psim_value, num_of_dimensions)
        result = kc_alt_value
    elif print_result == "print:all_in_list" or print_result == "all_in_list":
        psim_value = pSimSymId(kc, num_of_dimensions)
        pdsim_value = pDsimAsymUid(psim_value)
        kc_alt1_value = kc_alt1(psim_value, num_of_dimensions)
        kc_alt2_value = kc_alt2(psim_value, num_of_dimensions)
        kc_alt_value = kc_alt(kc, psim_value, num_of_dimensions)
        result = [
        kc,
        psim_value,
        pdsim_value,
        kc_alt1_value,
        kc_alt2_value,
        kc_alt_value
        ]
    elif print_result == "print:all_in_dict" or print_result == "all_in_dict":
        psim_value = pSimSymId(kc, num_of_dimensions)
        pdsim_value = pDsimAsymUid(psim_value)
        kc_alt1_value = kc_alt1(psim_value, num_of_dimensions)
        kc_alt2_value = kc_alt2(psim_value, num_of_dimensions)
        kc_alt_value = kc_alt(kc, psim_value, num_of_dimensions)
        result = {
        "kc": kc,
        "psim": psim_value,
        "pdsim": pdsim_value,
        "kc_alt1": kc_alt1_value,
        "kc_alt2": kc_alt2_value,
        "kc_alt": kc_alt_value
        }
    else:
        raise ValueError('Invalid print_result command. Please, use "print:kc", "print:psim", "print:pdsim", "print:kcalt1", "print:kcalt2", "print:kcalt", "print:all_in_list, or "print:all_in_dict" ')
    
    # Return the outcome(s) estimate based on the chosen result to print. 
    return result


def doc_isomorphic_optinalysis():
    print("""
    Performs Kabirian-based isomorphic optinalysis.

    This function processes two datasets (data_x, data_y) and a pairing type to generate an isoreflective list. The pairing type determines the arrangement of the data, 
    and then the Kabirian coefficient of optinalyis is calculated based on the dot product of the isoreflective list (bijective isomorphism) and an optiscale. 
    The result is a single estimate of Kabirian coefficient (kc) of similarity (relationship) between the two datasets. The kc value is then translated into probalitities
    and other alternate inverse or equivalent coefficients. The kc translations followed a systemetic Kabirian Y-rule of isomorphic optinalysis.    

    This function calculates several Kabirian-based isomorphic optinalysis estimates such as:
        - Kabirian coefficient of similarity (kc).
        - Probability of similarity (psim).
        - Probability of dissimilarity (pdsim).
        - Alternative Kabirian coefficients (kc_alt1, kc_alt2, kc_alt).
    
    Args:
        instruction_list (list): A list containing the following four elements:
            - data_x (list)   : First dataset for comparison.
            - data_y (list)   : Second dataset for comparison.
            - pairing (str)   : Specifies the pairing type. Options include: 
                * "pairing:H_H" or "H_H"    : For head-to-head (the lowest ends of the isoreflective pair of points are maximally distant).
                * "pairing:T_T" or "T_T"    : For tail-to-tail (the lowest ends of the isoreflective pair of points are minimally distant).
            - print_result (str) : Specifies the result to return. Options include:
                * "print:kc" or "kc"         : Prints the Kabirian coefficient of similarity.
                * "print:psim" or "psim"     : Prints the probability of similarity.
                * "print:pdsim" or "pdsim"   : Prints the probability of dissimilarity.
                * "print:kcalt1" or "kcalt1" : Prints the A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2" : Prints the D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"   : Prints the the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If an invalid pairing type or `print_result` option is provided.

    Examples:
        >>> import kbomodels as kbo
        >>> instruction_list = [[1, 0, 2, 4.25], [0, 5.47, 2.10, 90], "pairing:H_H", "print:kc"]
        >>> kbo.isomorphic_optinalysis(instruction_list)
        0.8419818140924717

        >>> instruction_list = [[1, 0, 2, 4.25], [0, 5.47, 2.10, 90], "pairing:T_T", "print:all_in_list"]
        >>> kc, psim, pdsim, kc_alt1, kc_alt2, kc_alt = kbo.isomorphic_optinalysis(instruction_list)
        >>> kc, psim, pdsim, kc_alt1, kc_alt2, kc_alt
        (0.5973738801376889, 0.08548645989747836, 0.9145135401025216, 0.5973738801376889, 3.0674236216785666, 3.0674236216785666)

    Process:
        1. The function first extracts data_x, data_y, and pairing type from the instruction_list.
        2. It generates an optiscale, which is a list of values from 0.01 to 2 times the length of data_x.
        3. Based on the pairing type ("H_H" or "T_T"), it creates an isoreflective list by combining data_x and data_y with a zero separator.
        4. Calculates the Kabirian coefficient (kc) through the `kc_isoptinalysis` function, which computes kc based on an isoreflective process of the data.
        5. Determines the number of dimensions (sample size) from the data.
        6. Selects the requested output based on `print_result` and computes the other additional estimates such as:
            * `psim`    : Probability of similarity, calculated from kc.
            * `pdsim`   : Probability of dissimilarity, calculated from psim.
            * `kc_alt1`, `kc_alt2`, and `kc_alt` : Alternative Kabirian coefficients using different formulas.
        7. Finally returns the result.

    References:
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)



# *****************************************************************************************************************************************************************
## Function for performing isomorphic optinalysis
# ******************************************************************************************************************************************************************
def automorphic_optinalysis(instruction_list: list) -> any:
    """
    Performs Kabirian-based isomorphic optinalysis.

    This function processes a single dataset by spliting it into two equal half as an 
    autoreflective pair. The Kabirian coefficient of optinalyis is calculated based on 
    the dot product of the autoreflective pair (bijective automorphism) and an optiscale. 
    The result is a single estimate of Kabirian coefficient (kc) of symmetry within the dataset. 
    The kc value is then translated into probalitities and other alternate inverse or equivalent 
    coefficients. The kc translations followed a systemetic Kabirian Y-rule of automorphic optinalysis.    

    This function calculates several Kabirian-based automorphic optinalysis estimates such as:
        - Kabirian coefficient of symmetry (kc),
        - Probability of symmetry (psym),
        - Probability of asymmetry (pasym),
        - Alternative Kabirian coefficients (kc_alt1, kc_alt2, kc_alt).

    Args:
        instruction_list (list) : A list containing two elements:
            - data (list) : A list of numerical values
            - print_result (str) : A string indicating which result(s) to return. Options include:
                * "print:kc" or "kc"          : Prints the Kabirian coefficient of symmetry.
                * "print:psym" or "psym"      : Prints the probability of symmetry.
                * "print:pasym" or "pasym"    : Prints the probability of asymmetry.
                * "print:kcalt1" or "kcalt1"  : Prints the A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2"  : Prints the D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"    : Prints the the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If an invalid `print_result` option is provided.

    Examples:
        >>> import kbomodels as kbo
        >>> data = [1, 2, 3, 4, 5, 6, 0, 6, 5, 4, 3, 2, 1]
        >>> instruction_list = [data, "print:psym"]
        >>> kbo.automorphic_optinalysis(instruction_list)
        1.0000

        >>> instruction_list = [data, "print:all_in_dict"]
        >>> kbo.automorphic_optinalysis(instruction_list)
        {'kc': 1.0, 'psym': 1.0, 'pasym': 0.0, 'kc_alt1': 1.0, 'kc_alt2': 1.0, 'kc_alt': 1.0}

    **Process:**
        1. Extracts the input data and the desired output from the instruction list.
        2. Calculates the Kabirian coefficient (kc) through the `kc_autoptinalysis` function, which computes kc based on an autoreflective process of the data.
        3. Determines the number of dimensions from the data.
        4. Selects the requested output based on `print_result` and computes the other additional estimates such as:
            * `psym` : Probability of symmetry, calculated from kc.
            * `pasym` : Probability of asymmetry, calculated from psym.
            * `kc_alt1`, `kc_alt2`, and `kc_alt` : Alternative Kabirian coefficients using different formulas.
        5. Finally returns the result.

    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Extracting data from the instruction_list
    data = instruction_list[0] # Data from the first list
    print_result = instruction_list[1] # Type of result(s) to print

    # Calculating the kc estimate of the automorphic optinalysis
    kc = kc_autoptinalysis(data)
    num_of_dimensions = int(len(data) / 2)
    
    # Calculating (translating) other estimates of automorphic optinalysis based on the selected result(s) to be printed from the print_result input
    if print_result == "print:kc" or print_result == "kc":
        result = kc
    elif print_result == "print:psym" or print_result == "psym":
        psym_value = pSimSymId(kc, num_of_dimensions)
        result = psym_value
    elif print_result == "print:pasym" or print_result == "pasym":
        psym_value = pSimSymId(kc, num_of_dimensions)
        pasym_value = pDsimAsymUid(psym_value)
        result = pasym_value
    elif print_result == "print:kcalt1" or print_result == "kcalt1":
        psym_value = pSimSymId(kc, num_of_dimensions)
        kc_alt1_value = kc_alt1(psym_value, num_of_dimensions)
        result = kc_alt1_value
    elif print_result == "print:kcalt2" or print_result == "kcalt2":
        psym_value = pSimSymId(kc, num_of_dimensions)
        kc_alt2_value = kc_alt2(psym_value, num_of_dimensions)
        result = kc_alt2_value
    elif print_result == "print:kcalt" or print_result == "kcalt":
        psym_value = pSimSymId(kc, num_of_dimensions)
        kc_alt_value = kc_alt(kc, psym_value, num_of_dimensions)
        result = kc_alt_value
    elif print_result == "print:all_in_list" or print_result == "all_in_list":
        psym_value = pSimSymId(kc, num_of_dimensions)
        pasym_value = pDsimAsymUid(psym_value)
        kc_alt1_value = kc_alt1(psym_value, num_of_dimensions)
        kc_alt2_value = kc_alt2(psym_value, num_of_dimensions)
        kc_alt_value = kc_alt(kc, psym_value, num_of_dimensions)
        result = [
        kc,
        psym_value,
        pasym_value,
        kc_alt1_value,
        kc_alt2_value,
        kc_alt_value
        ]
    elif print_result == "print:all_in_dict" or print_result == "all_in_dict":
        psym_value = pSimSymId(kc, num_of_dimensions)
        pasym_value = pDsimAsymUid(psym_value)
        kc_alt1_value = kc_alt1(psym_value, num_of_dimensions)
        kc_alt2_value = kc_alt2(psym_value, num_of_dimensions)
        kc_alt_value = kc_alt(kc, psym_value, num_of_dimensions)
        result = {
        "kc": kc,
        "psym": psym_value,
        "pasym": pasym_value,
        "kc_alt1": kc_alt1_value,
        "kc_alt2": kc_alt2_value,
        "kc_alt": kc_alt_value
        }
    else:
        raise ValueError('Invalid print_result command. Please, use "print:kc", "print:psym", "print:pasym", "print:kcalt1", "print:kcalt2", "print:kcalt", "print:all_in_list, or "print:all_in_dict" ')
    
    # Return the outcome(s) estimate based on the chosen result to print. 
    return result


def doc_automorphic_optinalysis():
    print("""
    Performs Kabirian-based isomorphic optinalysis.

    This function processes a single dataset by spliting it into two equal half as an 
    autoreflective pair. The Kabirian coefficient of optinalyis is calculated based on 
    the dot product of the autoreflective pair (bijective automorphism) and an optiscale. 
    The result is a single estimate of Kabirian coefficient (kc) of symmetry within the dataset. 
    The kc value is then translated into probalitities and other alternate inverse or equivalent 
    coefficients. The kc translations followed a systemetic Kabirian Y-rule of automorphic optinalysis.    

    This function calculates several Kabirian-based automorphic optinalysis estimates such as:
        - Kabirian coefficient of symmetry (kc),
        - Probability of symmetry (psym),
        - Probability of asymmetry (pasym),
        - Alternative Kabirian coefficients (kc_alt1, kc_alt2, kc_alt).

    Args:
        instruction_list (list) : A list containing two elements:
            - data (list) : A list of numerical values
            - print_result (str) : A string indicating which result(s) to return. Options include:
                * "print:kc" or "kc"          : Prints the Kabirian coefficient of symmetry.
                * "print:psym" or "psym"      : Prints the probability of symmetry.
                * "print:pasym" or "pasym"    : Prints the probability of asymmetry.
                * "print:kcalt1" or "kcalt1"  : Prints the A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2"  : Prints the D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"    : Prints the the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If an invalid `print_result` option is provided.

    Examples:
        >>> import kbomodels as kbo
        >>> data = [1, 2, 3, 4, 5, 6, 0, 6, 5, 4, 3, 2, 1]
        >>> instruction_list = [data, "print:psym"]
        >>> kbo.automorphic_optinalysis(instruction_list)
        1.0000

        >>> instruction_list = [data, "print:all_in_dict"]
        >>> kbo.automorphic_optinalysis(instruction_list)
        {'kc': 1.0, 'psym': 1.0, 'pasym': 0.0, 'kc_alt1': 1.0, 'kc_alt2': 1.0, 'kc_alt': 1.0}

    Process:
        1. Extracts the input data and the desired output from the instruction list.
        2. Calculates the Kabirian coefficient (kc) through the `kc_autoptinalysis` function, which computes kc based on an autoreflective process of the data.
        3. Determines the number of dimensions from the data.
        4. Selects the requested output based on `print_result` and computes the other additional estimates such as:
            * `psym` : Probability of symmetry, calculated from kc.
            * `pasym` : Probability of asymmetry, calculated from psym.
            * `kc_alt1`, `kc_alt2`, and `kc_alt` : Alternative Kabirian coefficients using different formulas.
        5. Finally returns the result.

    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)



# *****************************************************************************************************************************************************************
## Function for estimating the symmetry and asymmetry of a data using a customized, and optimized Kabirian-based automorphic optinalysis
# ******************************************************************************************************************************************************************
def stat_SymAsymmetry(instruction_list: list) -> any:
    """
    Estimates the symmetry and asymmetry of a dataset using a customized, and optimized Kabirian-based automorphic optinalysis.

    This function takes a dataset, preprocesses it by centering and ordering, and then applies 
    a customized Kabirian automorphic optinalysis to evaluate its symmetry or asymmetry. The user 
    can specify the method for centering and ordering the data before the analysis. Symmetry and asymmetry 
    are calculated based on the transformation of the preprocessed data.

    Args:
        instruction_list (list): A list containing the following elements:
            - data (list): The input dataset to be analyzed for symmetry and asymmetry.
            - centering (str): Method for centering the data. Options include:
                * "centering:bymean" or "bymean"     : Center the data by its mean.
                * "centering:bymedian" or "bymedian" : Center the data by its median.
                * "centering:bymode" or "bymode"     : Center the data by its mode.
                * Custom numeric value for user-defined centering.
            - ordering (str): Method for ordering the data. Options include:
                * "ordering:ascend" or"ascend"       : Sort the data in ascending order.
                * "ordering:descend" or "descend"    : Sort the data in descending order.
            - print_result (str): Specifies the result to return from automorphic optinalysis. Options may include:
                * "print:kc" or "kc"        : Prints Kabirian coefficient.
                * "print:psym" or "psym"    : Prints probability of symmetry.
                * "print:pasym" or "pasym"  : Prints probability of asymmetry.
                * "print:all_in_list" or "all_in_list"   : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"   : Prints all computed estimates in a dictionary.
    
    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.
    
    Raises:
        ValueError: If an invalid centering method, ordering method, or `print_result` option is provided.

    Examples:
        >>> import kbomodels as kbo
        >>> instruction_list = [[1.5, 2.0, 3.5, 4.0, 5.5], "centering:bymean", "ordering:ascend", "print:psym"]
        >>> kbo.stat_SymAsymmetry(instruction_list)
        0.9682539682539683
    
        >>> instruction_list = [[3.2, 4.1, 2.7, 5.0], "centering:bymedian", "ordering:descend", "print:all_in_dict"]
        >>> kbo.stat_SymAsymmetry(instruction_list)
        {'kc': 1.0810810810810811,
        'psym': 0.7977528089887641,
        'pasym': 0.2022471910112359}
    
    **Process:**
        1. The function first preprocesses the input data by centering it according to the user's specified method 
           (mean, median, mode or a user-define value) and ordering it in ascending or descending order.
        2. The preprocessed data is then converted into absolute values.
        3. A Kabirian-based automorphic optinalysis is performed on the transformed data to evaluate its symmetry 
           and asymmetry.
        4. The selected result from the analysis is returned based on the user's input command (`print_result`).
    
    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2022). Some estimators and their properties following Kabirian-based optinalysis.  
        Preprints.org, 2022100464. doi:10.20944/preprints202210.0464.v1
    """
    # Extracting data from the instruction_list
    data = instruction_list[0]
    centering = instruction_list[1]
    ordering = instruction_list[2]
    print_result = instruction_list[3]
    
    # Function for customized preporocessing of the data prior to automorphic optinalysis
    def preporocessing(instruction_list):
        # Extracting data from the instruction_list
        data = instruction_list[0]
        centering = instruction_list[1]
        ordering = instruction_list[2]

        # centering of data of the variable based on the input command 
        if centering == "centering:bymean" or centering == "bymean":
            data_centered = np.array(data) - np.mean(data)
        elif centering == "centering:bymedian" or centering == "bymedian":
            data_centered = np.array(data) - np.median(data)
        elif centering == "centering:bymode" or centering == "bymode":
            data_centered = np.array(data) - statistics.mode(data)
        elif isinstance(centering, (int, float)):
            reference_value = centering
            data_centered = np.array(data) - [reference_value]
        else:
            raise ValueError ('please use "centering:bymean" or "bymean", "centering:bymedian" or "bymedian", "centering:bymode" or "bymode", by a reference value to command centering') 

        # ordering of data of the variable based on the input command
        if ordering == "ordering:ascend" or ordering == "ascend":
            data_ordered = sorted(data_centered)
        elif ordering == "ordering:descend" or ordering == "descend":
            data_ordered = sorted(data_centered)[::-1]
        else:
            raise ValueError ('please, use "ordering:ascend" or "ascend", "ordering:descend" or "descend" to command ordering')

        # absolute values of the outcome after centering and/or ordering of data of the variables
        data_1 = abs(np.array(data_ordered))
        return data_1
    
    # customized preporocessing of the data prior to automorphic optinalysis
    data_shaped = preporocessing([data, centering, ordering])
    
    # Perform Kabirian-based automorphic analysis on the preprocessed data
    outcomes = automorphic_optinalysis([data_shaped, print_result])

    # Return the outcome(s) based on the chosen result to print.
    if print_result == "print:all_in_dict" or print_result == "all_in_dict":
        for key in list(outcomes)[3:]:
            outcomes.pop(key)
            outcomesx = outcomes
    elif print_result == "print:all_in_list" or print_result == "all_in_list":
        outcomesx = outcomes[:3]
    else:
        outcomesx = outcomes
    
    # Return the outcome(s) estimate based on the chosen result to print. 
    return outcomesx


def doc_stat_SymAsymmetry():
    print("""
    Estimates the symmetry and asymmetry of a dataset using a customized, and optimized Kabirian-based automorphic optinalysis.

    This function takes a dataset, preprocesses it by centering and ordering, and then applies 
    a customized Kabirian automorphic optinalysis to evaluate its symmetry or asymmetry. The user 
    can specify the method for centering and ordering the data before the analysis. Symmetry and asymmetry 
    are calculated based on the transformation of the preprocessed data.

    Args:
        instruction_list (list): A list containing the following elements:
            - data (list): The input dataset to be analyzed for symmetry and asymmetry.
            - centering (str): Method for centering the data. Options include:
                * "centering:bymean" or "bymean"     : Center the data by its mean.
                * "centering:bymedian" or "bymedian" : Center the data by its median.
                * "centering:bymode" or "bymode"     : Center the data by its mode.
                * Custom numeric value for user-defined centering.
            - ordering (str): Method for ordering the data. Options include:
                * "ordering:ascend" or"ascend"       : Sort the data in ascending order.
                * "ordering:descend" or "descend"    : Sort the data in descending order.
            - print_result (str): Specifies the result to return from automorphic optinalysis. Options may include:
                * "print:kc" or "kc"        : Prints Kabirian coefficient.
                * "print:psym" or "psym"    : Prints probability of symmetry.
                * "print:pasym" or "pasym"  : Prints probability of asymmetry.
                * "print:all_in_list" or "all_in_list"   : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"   : Prints all computed estimates in a dictionary.
    
    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.
    
    Raises:
        ValueError: If an invalid centering method, ordering method, or `print_result` option is provided.

    Examples:
        >>> import kbomodels as kbo
        >>> instruction_list = [[1.5, 2.0, 3.5, 4.0, 5.5], "centering:bymean", "ordering:ascend", "print:psym"]
        >>> kbo.stat_SymAsymmetry(instruction_list)
        0.9682539682539683
    
        >>> instruction_list = [[3.2, 4.1, 2.7, 5.0], "centering:bymedian", "ordering:descend", "print:all_in_dict"]
        >>> kbo.stat_SymAsymmetry(instruction_list)
        {'kc': 1.0810810810810811,
        'psym': 0.7977528089887641,
        'pasym': 0.2022471910112359}
    
    Process:
        1. The function first preprocesses the input data by centering it according to the user's specified method 
           (mean, median, mode or a user-define value) and ordering it in ascending or descending order.
        2. The preprocessed data is then converted into absolute values.
        3. A Kabirian-based automorphic optinalysis is performed on the transformed data to evaluate its symmetry 
           and asymmetry.
        4. The selected result from the analysis is returned based on the user's input command (`print_result`).
    
    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2022). Some estimators and their properties following Kabirian-based optinalysis.  
        Preprints.org, 2022100464. doi:10.20944/preprints202210.0464.v1  
    """)



# *****************************************************************************************************************************************************************
## Function for performing pairwise analysis of biological sequences using a customized, and optimized Kabirian-based isomorphic optinalysis.
# ******************************************************************************************************************************************************************
def bioseq_gpa(instruction_list: list) -> any:
    """
    Perform pairwise sequence analysis of aligned biological sequences using a customized, and optimized Kabirian-based isomorphic optinalysis.

    This function computes the Kabirian coefficient (kc) and other similarity metrics (psim, pdsim, kc_alt1, kc_alt2, kc_alt) 
    between two aligned biological sequences (DNA, RNA, or Protein). It encodes the sequences based on the specified encoding scheme 
    and performs either head-to-head (H_H) or tail-to-tail (T_T) sequence pairing, depending on user input.

    Args:
        instruction_list (list) : A list of five elements containing the following:
            - sequence_x (str)      : The first sequence (DNA, RNA, or Protein).
            - sequence_y (str)      : The second sequence (DNA, RNA, or Protein).
            - encoding_scheme (str) : The type of encoding to be applied. Options are:
                * "seq_type:DNA" or "DNA"           : for DNA sequences.
                * "seq_type:RNA" or "RNA"           : for RNA sequences.
                * "seq_type:protein" or "protein"   : for Protein sequences.
            - pairing (str)         : The type of sequence pairing to be used for alignment. Options are:
                * "pairing:H_H" or "H_H"        : For head-to-head pairing.
                * "pairing:T_T" or "T_T"        : For tail-to-tail pairing.
            - print_result (str)    : The specific result to print. Options are:
                * "print:kc" or "kc"            : Prints the Kabirian coefficient.
                * "print:psim" or "psim"        : Prints the probability of similarity.
                * "print:pdsim" or "pdsim"      : Prints the probability of dissimilarity.
                * "print:kcalt1" or "kcalt1"    : Prints the A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2"    : Prints the D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"      : Prints the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"    : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"    : Prints all computed estimates in a dictionary.
    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If the input data is not properly formatted or does not match the expected structure.

    Examples:
        >>> import kbomodels as kbo
        >>> # DNA sequence comparison on head-to-head pairing and all results print 
        >>> seq1 = 'AGTA-AGC-AA'
        >>> seq2 = 'AGTA-AGCGTT'
        >>> kbo.bioseq_gpa([seq1, seq2, 'seq_type:DNA', 'pairing:H_H', 'print:all_in_dict'])
        {'kc': 0.9863277488927401,
        'psim': 0.9702066650347937,
        'pdsim': 0.02979333496520631,
        'kc_alt1': 0.9863277488927401,
        'kc_alt2': 1.014056622451,
        'kc_alt': 1.014056622451}

        >>> # Protein sequence comparison with tail-to-tail pairing and all results print
        >>> seq3 = 'GD-QFR-'
        >>> seq4 = 'GD-QSHF'
        >>> kc, psim, pdsim, kc_alt1, kc_alt2, kc_alt = kbo.bioseq_gpa([seq3, seq4, 'seq_type:protein', 'pairing:T_T', 'print:all_in_list])
        kc, psim, pdsim, kc_alt1, kc_alt2, kc_alt
        (0.9408005113046257,
        0.8658216387505657,
        0.13417836124943427,
        0.9408005113046256,
        1.067149977344812,
        1.067149977344812)

    **Notes:**
        1. The function encodes the sequences numerically based on the provided encoding scheme.
        2. It calculates estimates based on the Kabirian-based isomorphic optinalysis and allows for flexible result output.
        3. Invalid input commands for pairing or encoding scheme will prompt an error message.
        4. The function is extensible for various types of sequence comparisons used in fields like bioinformatics and genetics.
    
    **References:**
        *Cite this reference to acknowledge the methodology:*
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite this reference to acknowledge the Python code implementation of the methodology:*
        Abdullahi, K. B. (2024). Python code for geometrical pairwise analysis of biological sequences following Kabirian-based isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/tnwpt54jnb.3 (https://data.mendeley.com/datasets/tnwpt54jnb/3).
    """

    # Extracting data from the instruction_list
    sequence_x = instruction_list[0]  # Data from the first list
    sequence_y = instruction_list[1]  # Data from the second list
    encoding_scheme = instruction_list[2] # Encoding scheme
    pairing = instruction_list[3] # Type of pairing
    print_result = instruction_list[4] # Type of result(s) to print
    
    # Numerical encoding scheme for DNA sequences
    def DNA_encoding(seq):
        encoding = {'c': 111, 't': 126, 'a': 135, 'g': 151, '-': 0, 'C': 111, 'T': 126, 'A': 135, 'G': 151,}
        return [encoding.get(n, 0) for n in seq]

    # Numerical encoding scheme for RNA sequences
    def RNA_encoding(seq):
        encoding = {'c': 111, 'u': 112, 'a': 135, 'g': 151, '-': 0, 'C': 111, 'U': 112, 'A': 135, 'G': 151}
        return [encoding.get(n, 0) for n in seq]

    # Numerical encoding scheme for protein sequences
    def protein_encoding(seq):
        encoding = {'G': 75, 'A': 89, 'S': 105, 'P': 115, 'V': 117, 'T': 119, 'C': 121, 'I': 131, 'L': 131, 'N': 132, 
                    'D': 133, 'Q': 146, 'K': 146, 'E': 147, 'M': 149, 'H': 155, 'F': 165, 'R': 174, 'Y': 181, 'W': 204,
                   'g': 75, 'a': 89, 's': 105, 'p': 115, 'v': 117, 't': 119, 'c': 121, 'i': 131, 'l': 131, 'n': 132, 
                    'd': 133, 'q': 146, 'k': 146, 'e': 147, 'm': 149, 'h': 155, 'f': 165, 'r': 174, 'y': 181, 'W': 204, '-': 0}
        return [encoding.get(n, 0) for n in seq]

    # Encoding Sequences Based on the Selected Encoding Scheme
    if encoding_scheme == "seq_type:DNA" or encoding_scheme == "DNA":
        seq_1 = DNA_encoding(sequence_x)
        seq_2 = DNA_encoding(sequence_y)
    elif encoding_scheme == "seq_type:RNA" or encoding_scheme == "RNA":
        seq_1 = RNA_encoding(sequence_x)
        seq_2 = RNA_encoding(sequence_y)
    elif encoding_scheme == "seq_type:protein" or encoding_scheme == "protein":
        seq_1 = protein_encoding(sequence_x)
        seq_2 = protein_encoding(sequence_y)
    else:
        raise ValueError ('Invalid command. Please use "seq_type:DNA", "seq_type:RNA", or "seq_type:protein" to command encoding_scheme.')
    
    # Kabirian-based isomorphic optinalysis model calculations.
    outcome = isomorphic_optinalysis([seq_1, seq_2, pairing, print_result])
    
    # Return the outcome(s) based on the chosen result to print. 
    return outcome


def doc_bioseq_gpa():
    print("""
    Perform pairwise sequence analysis of aligned biological sequences using a customized, and optimized Kabirian-based isomorphic optinalysis.

    This function computes the Kabirian coefficient (kc) and other similarity metrics (psim, pdsim, kc_alt1, kc_alt2, kc_alt) 
    between two aligned biological sequences (DNA, RNA, or Protein). It encodes the sequences based on the specified encoding scheme 
    and performs either head-to-head (H_H) or tail-to-tail (T_T) sequence pairing, depending on user input.

    Args:
        instruction_list (list) : A list of five elements containing the following:
            - sequence_x (str)      : The first sequence (DNA, RNA, or Protein).
            - sequence_y (str)      : The second sequence (DNA, RNA, or Protein).
            - encoding_scheme (str) : The type of encoding to be applied. Options are:
                * "seq_type:DNA" or "DNA"           : for DNA sequences.
                * "seq_type:RNA" or "RNA"           : for RNA sequences.
                * "seq_type:protein" or "protein"   : for Protein sequences.
            - pairing (str)         : The type of sequence pairing to be used for alignment. Options are:
                * "pairing:H_H" or "H_H"        : For head-to-head pairing.
                * "pairing:T_T" or "T_T"        : For tail-to-tail pairing.
            - print_result (str)    : The specific result to print. Options are:
                * "print:kc" or "kc"            : Prints the Kabirian coefficient.
                * "print:psim" or "psim"        : Prints the probability of similarity.
                * "print:pdsim" or "pdsim"      : Prints the probability of dissimilarity.
                * "print:kcalt1" or "kcalt1"    : Prints the A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2"    : Prints the D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"      : Prints the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"    : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"    : Prints all computed estimates in a dictionary.
    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If the input data is not properly formatted or does not match the expected structure.

    Examples:
        >>> import kbomodels as kbo
        >>> # DNA sequence comparison on head-to-head pairing and all results print 
        >>> seq1 = 'AGTA-AGC-AA'
        >>> seq2 = 'AGTA-AGCGTT'
        >>> kbo.bioseq_gpa([seq1, seq2, 'seq_type:DNA', 'pairing:H_H', 'print:all_in_dict'])
        {'kc': 0.9863277488927401,
        'psim': 0.9702066650347937,
        'pdsim': 0.02979333496520631,
        'kc_alt1': 0.9863277488927401,
        'kc_alt2': 1.014056622451,
        'kc_alt': 1.014056622451}

        >>> # Protein sequence comparison with tail-to-tail pairing and all results print
        >>> seq3 = 'GD-QFR-'
        >>> seq4 = 'GD-QSHF'
        >>> kc, psim, pdsim, kc_alt1, kc_alt2, kc_alt = kbo.bioseq_gpa([seq3, seq4, 'seq_type:protein', 'pairing:T_T', 'print:all_in_list])
        kc, psim, pdsim, kc_alt1, kc_alt2, kc_alt
        (0.9408005113046257,
        0.8658216387505657,
        0.13417836124943427,
        0.9408005113046256,
        1.067149977344812,
        1.067149977344812)

    Notes:
        1. The function encodes the sequences numerically based on the provided encoding scheme.
        2. It calculates estimates based on the Kabirian-based isomorphic optinalysis and allows for flexible result output.
        3. Invalid input commands for pairing or encoding scheme will prompt an error message.
        4. The function is extensible for various types of sequence comparisons used in fields like bioinformatics and genetics.
    
    References:
        Cite this reference to acknowledge the methodology:
        Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        Abdullahi, K. B. (2024). Python code for geometrical pairwise analysis of biological sequences following Kabirian-based isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/tnwpt54jnb.3 (https://data.mendeley.com/datasets/tnwpt54jnb/3).
    """) 



# ******************************************************************************************************************************************************************
## Function for performing statistical dispersion estimations on a dataset using a parameterized, customized, and optimized Kabirian-based isomorphic optinalysis.
# *****************************************************************************************************************************************************************
def stat_mirroring(instruction_list: list) -> any:
    """
    Performs statistical dispersion estimations on a dataset using a parameterized, customized, and optimized Kabirian-based isomorphic optinalysis.

    Estimates statistical dispersion from a defined centre using customized centering, ordering, and other statistical mirroring principles. It is a parameterized and customized application of 
    Kabirian-based isomorphic optinalysis. It computes the Kabirian coefficient of proximity (kc), probability of proximity (pprox), probability of deviation (pdev), and alternate Kabirian coefficients (kc_alt1, kc_alt2). 
    This is based on the transformed dataset and its statistical mirror.

    The process of statistical mirroring comprises two distinct phases:
        a)	Preprocessing phase **[Ref_1]**: This involves applying preprocessing transformations, such as compulsory theoretical ordering, with or without centering the data. 
        It also encompasses tasks like statistical mirror design and optimizations within the established optinalytic construction. These optimizations include selecting an 
        efficient pairing style, central normalization, and establishing an isoreflective pair between the preprocessed data and its designed statistical mirror. 
        b)	Optinalytic model calculation phase **[Ref_2]**: This phase is focused on computing estimates (such as the Kabirian coefficient of proximity, 
        the probability of proximity, and the deviation) based on Kabirian-based isomorphic optinalysis models. 

    Args:
        instruction_list (list) : A list of instructions that includes the following six elements:
            - instruction_list[0] : array-like
                The dataset to be analyzed.
            - instruction_list[1] : str or numeric
                The principal value used for mirror design. Can be one of the following strings:
                * "principal_value:mean" or "mean"        : Here, the mean of the trnasformed data constructs the statistical mirror.
                * "principal_value:median" or "median"    : Here, the median of the trnasformed data constructs the statistical mirror.
                * "principal_value:mode" or "mode"        : Here, the mode of the trnasformed data constructs the statistical mirror.
                * "principal_value:maximum" or "maximum"  : Here, the maximum of the trnasformed data constructs the statistical mirror.
                * "principal_value:minimum" "minimum"     : Here, the minimum of the trnasformed data constructs the statistical mirror.
                * a custom numeric value                  : Here, the provided numeric value constructs the statistical mirror.
            - instruction_list[2] : str or numeric
                The centering method. Options include:
                * "centering:never"     : No centering applied.
                * "centering:bymean*", or "centering:bymeanR+"       : Center by mean and return absolute positive values.
                * "centering:bymedian*", or "centering:bymedianR+"   : Center by median and return absolute positive values.
                * "centering:bymode*", or "centering:bymodeR+"       : Center by mode and return absolute positive values.
                * "centering:bymaximum*", or "centering:bymaximumR+" : Center by maximum and return absolute positive values.
                * "centering:byminimum*", or "centering:byminimumR+" : Center by minimum and return absolute positive values.
                * "centering:bymean", or "centering:bymeanR∓"        : Center by mean without absolute values.
                * "centering:bymedian", or "centering:bymedianR∓"    : Center by median without absolute values.
                * "centering:bymode", or "centering:bymodeR∓"        : Center by mode without absolute values.
                * "centering:bymaximum", or "centering:bymaximumR∓"  : Center by maximum without absolute values.
                * "centering:byminimum", or "centering:byminimumR∓"  : Center by minimum without absolute values.
                * "centering:bymean#", or "centering:bymeanR-"       : Center by mean and return absolute negative values.
                * Custom numeric value for user-defined centering.
                    > Note: You can ignore the 'centering: ' word. For instance: "centering:never" as "never" in its specific order.
            - instruction_list[3] : str
                The ordering method. Options include:
                * "ordering:ascend" or "ascend"     : Sort data in ascending order.
                * "ordering:descend" or "descend"   : Sort data in descending order.
            - instruction_list[4] : str
                Pairing method for isomorphic optinalysis. Options include:
                * "pairing:H_H" or "H_H"    : For head-to-head (the lowest ends of the isoreflective pair of points are maximally distant).
                * "pairing:T_T" or "T_T"    : For tail-to-tail (the lowest ends of the isoreflective pair of points are minimally distant).
            - instruction_list[5] : str
                Specifies the result to return. Options include: 
                * "print:kc" or "kc"          : Prints Kabirian coefficient of proximity.
                * "print:pprox" or "pprox"    : Prints probability of proximity.
                * "print:pdev" or "pdev"      : Prints probability of deviation.
                * "print:kcalt1" or "kcalt1"  : Prints A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2"  : Prints D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"    : Prints the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises: 
        ValueError
            If invalid values are provided for centering, ordering, or the principal value for the mirror design.

    Examples:
        >>> import kbomodels as kbo
        >>> data = [-8.89, 47.91, 122.87, -3.02, -2.68, 60.17, 30.3, 113.62]

        >>> # Example 1: Absolute meanic mirroring (Scaloc-invariant estimation)
        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:bymean*", "ordering:ascend", "pairing:H_H", "print:kc"])
        0.9285721008593181

        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:bymean*", "ordering:ascend", "pairing:H_H", "print:pprox"])
        0.840709450595581

        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:bymean*", "ordering:ascend", "pairing:H_H", "print:pdev"])
        0.159290549404419

        >>> # Example 2: Raw meanic mirroring (Scale-invariant estimation)
        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:never", "ordering:ascend", "pairing:H_H", "print:kc"])
        0.8834145225095626

        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:never*", "ordering:ascend", "pairing:H_H", "print:pprox"])
        0.7414505643231742

        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:never*", "ordering:ascend", "pairing:H_H", "print:pdev"])
        0.25854943567682576

        >>> # Example 3: Raw maximalic mirroring
        >>> kbo.stat_mirroring([data, "principal_value:maximum", "centering:never", "ordering:ascend", "pairing:H_H", "print:kc"])
        0.7677090199694419

        >>> kbo.stat_mirroring([data, "principal_value:maximum", "centering:never", "ordering:ascend", "pairing:H_H", "print:pprox"])
        0.49209306975510636

        >>> kbo.stat_mirroring([data, "principal_value:maximum", "centering:never", "ordering:ascend", "pairing:H_H", "print:pdev"])
        0.5079069302448936

    **Notes:**
        This function performs three main steps:
        1. **Preprocessing**: The data is centered, ordered, and transformed according to the specified instructions.
        2. **Mirror Design**: A statistical mirror is established based on the principal value (mean, median, mode, maximum, minimun, or any other defined location estimate).
        3. **Optinalytic Model Calculation**: Kabirian-based Isomorphic optinalysis is applied between the preprocessed data and its statistical mirror to estimate the statistical dispersion.

        The Statistical Mirroring function is highly customizable, allowing users to define various centering methods, mirror designs, ordering, and pairing styles to meet their analysis needs. 
        For user-specific invariance tasks, the scaloc and scale invariance properties of the estimation outcomes are solely determined by the decision to apply or skip the centering process, respectively.
    
    **Key Concepts:**
            - **Kabirian coefficient of proximity (kc)**: A measure of the coefficient of dispersion from the defined center.
            - **Probability of proximity (pprox)**: The likelihood that data points are closely dispersed around a defined center.
            - **Probability of deviation (pdev)**: The likelihood that data points are distantly dispersed around a defined center.
            - **Alternate Kabirian coefficients**: The alternate Kabirian coefficients such as kcalt1, kcalt2, kcalt. 

    **References:**
        *Cite these references to acknowledge the methodologies:* 
        **[Ref_1]** Abdullahi, K. B. (2024). Statistical mirroring: A robust method for statistical dispersion estimation. 
        MethodsX, 12, 102682. https://doi.org/10.1016/j.mex.2024.102682 
        
        **[Ref_2]** Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite these references to acknowledge the Python codes implementation of the methodologies:*
        **[Ref_1]** Abdullahi, K. B. (2024). A Python Code for statistical mirroring. Mendeley Data, V4. 
        doi: 10.17632/ppfvc65m2v.4 (https://data.mendeley.com/datasets/ppfvc65m2v/4)

        **[Ref_2]** Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Extracting data from the instruction_list
    data = instruction_list[0]
    mirror_principal_value = instruction_list[1]
    centering = instruction_list[2]
    ordering = instruction_list[3]
    pairing = instruction_list[4]
    print_result = instruction_list[5]
    
    # Function for performing isomorphic optinalysis
    def isomorphic_optinalysis_(instruction_list: list) -> any:
        # Extracting input data from the instruction_list
        data_x = instruction_list[0]  
        data_y = instruction_list[1] 
        pairing = instruction_list[2]  
        print_result = instruction_list[3] 
        
        # Calculating the kc estimate of the isomorphic optinalysis
        kc = kc_isoptinalysis(instruction_list)
        num_of_dimensions = len(data_x)
        
        # Calculating (translating) other estimates of isomorphic optinalysis based on the selected result(s) to be printed from the print_result input
        if print_result == "print:kc" or print_result == "kc":
            result = kc
        elif print_result == "print:pprox" or print_result == "pprox":
            pprox_value = pSimSymId(kc, num_of_dimensions)
            result = pprox_value
        elif print_result == "print:pdev" or print_result == "pdev":
            pprox_value = pSimSymId(kc, num_of_dimensions)
            pdev_value = pDsimAsymUid(pprox_value)
            result = pdev_value
        elif print_result == "print:kcalt1" or print_result == "kcalt1":
            pprox_value = pSimSymId(kc, num_of_dimensions)
            kc_alt1_value = kc_alt1(pprox_value, num_of_dimensions)
            result = kc_alt1_value
        elif print_result == "print:kcalt2" or print_result == "kcalt2":
            pprox_value = pSimSymId(kc, num_of_dimensions)
            kc_alt2_value = kc_alt2(pprox_value, num_of_dimensions)
            result = kc_alt2_value
        elif print_result == "print:kcalt" or print_result == "kcalt":
            pprox_value = pSimSymId(kc, num_of_dimensions)
            kc_alt_value = kc_alt(kc, pprox_value, num_of_dimensions)
            result = kc_alt_value
        elif print_result == "print:all_in_list" or print_result == "all_in_list":
            pprox_value = pSimSymId(kc, num_of_dimensions)
            pdev_value = pDsimAsymUid(pprox_value)
            kc_alt1_value = kc_alt1(pprox_value, num_of_dimensions)
            kc_alt2_value = kc_alt2(pprox_value, num_of_dimensions)
            kc_alt_value = kc_alt(kc, pprox_value, num_of_dimensions)
            result = [
            kc,
            pprox_value,
            pdev_value,
            kc_alt1_value,
            kc_alt2_value,
            kc_alt_value
            ]
        elif print_result == "print:all_in_dict" or print_result == "all_in_dict":
            pprox_value = pSimSymId(kc, num_of_dimensions)
            pdev_value = pDsimAsymUid(pprox_value)
            kc_alt1_value = kc_alt1(pprox_value, num_of_dimensions)
            kc_alt2_value = kc_alt2(pprox_value, num_of_dimensions)
            kc_alt_value = kc_alt(kc, pprox_value, num_of_dimensions)
            result = {
            "kc": kc,
            "pprox": pprox_value,
            "pdev": pdev_value,
            "kc_alt1": kc_alt1_value,
            "kc_alt2": kc_alt2_value,
            "kc_alt": kc_alt_value
            }
        else:
            raise ValueError('Invalid print_result command. Please, use "print:kc", "print:pprox", "print:pdev", "print:kcalt1", "print:kcalt2", "print:kcalt", "print:all_in_list, or "print:all_in_dict" ')
        return result

    ## Preprocessing stage, which involve centering and ordering transformation of the dataset, and as well as statistical mirror designs prior for isomorphic optinalysis.
    # Function for customized preporocessing transformations of the data prior to isomorphic optinalysis
    def preprocessing(instruction_list):
        # Extracting data from the instruction_list
        data = instruction_list[0]
        mirror_principal_value = instruction_list[1]
        centering = instruction_list[2]
        ordering = instruction_list[3]
        
        # Centering not allowed 
        if centering == "centering:never" or centering == "never":
            data_centered = data
            
        # Centering of data of the variable based on the input command with returning absolute positive values 
        elif centering == "centering:bymean*" or centering == "centering:bymeanR+" or centering == "bymean*" or centering == "bymeanR+":
            data_centered = abs(np.array(data) - np.mean(data))
        elif centering == "centering:bymedian*" or centering == "centering:bymedianR+" or centering == "bymedian*" or centering == "bymedianR+":
            data_centered = abs(np.array(data) - np.median(data))
        elif centering == "centering:bymode*" or centering == "centering:bymodeR+" or centering == "bymode*" or centering == "bymodeR+":
            data_centered = abs(np.array(data) - statistics.mode(data))
        elif centering == "centering:bymaximum*" or centering == "centering:bymaximumR+" or centering == "bymaximum*" or centering == "bymaximumR+":
            data_centered = abs(np.array(data) - np.max(data))
        elif centering == "centering:byminimum*" or centering == "centering:byminimumR+" or centering == "byminimum*" or centering == "byminimumR+":
            data_centered = abs(np.array(data) - np.min(data)) 

        # Centering of data of the variable based on the input command without returning absolute values 
        elif centering == "centering:bymean" or centering == "centering:bymeanR∓" or centering == "bymean" or centering == "bymeanR∓":
            data_centered = np.array(data) - np.mean(data)
        elif centering == "centering:bymedian" or centering == "centering:bymedianR∓" or centering == "bymedian" or centering == "bymedianR∓":
            data_centered = np.array(data) - np.median(data)
        elif centering == "centering:bymode" or centering == "centering:bymodeR∓" or centering == "bymode" or centering == "bymodeR∓":
            data_centered = np.array(data) - statistics.mode(data)
        elif centering == "centering:bymaximum" or centering == "centering:bymaximumR∓" or centering == "bymaximum" or centering == "bymaximumR∓":
            data_centered = np.array(data) - np.max(data)
        elif centering == "centering:byminimum" or centering == "centering:byminimumR∓" or centering == "byminimum" or centering == "byminimumR∓":
            data_centered = np.array(data) - np.min(data)
        
        # Centering of data of the variable based on the input command with returning absolute negative values 
        elif centering == "centering:bymean#" or centering == "centering:bymeanR-" or centering == "bymean#" or centering == "bymeanR-":
            data_centered = -1 * abs(np.array(data) - np.mean(data))
        elif centering == "centering:bymedian#" or centering == "centering:bymedianR-" or centering == "bymedian#" or centering == "bymedianR-":
            data_centered = -1 * abs(np.array(data) - np.median(data))
        elif centering == "centering:bymode#" or centering == "centering:bymodeR-" or centering == "bymode#" or centering == "bymodeR-":
            data_centered = -1 * abs(np.array(data) - statistics.mode(data))
        elif centering == "centering:bymaximum#" or centering == "centering:bymaximumR-" or centering == "bymaximum#" or centering == "bymaximumR-":
            data_centered = -1 * abs(np.array(data) - np.max(data))
        elif centering == "centering:byminimum#" or centering == "centering:byminimumR-" or centering == "byminimum#" or centering == "byminimumR-":
            data_centered = -1 * abs(np.array(data) - np.min(data)) 
        elif isinstance(centering, (int, float)):
            reference_value = centering
            data_centered = np.array(data) - [reference_value]
        else:
            raise ValueError ( 'Invalid centering command. Please use: "centering:bymeanR+ or centering:bymean*", "centering:bymedianR+ or centering:bymedian*", "centering:bymodeR+ or centering:bymode*", "centering:bymaximumR+ or centering:bymaximum*", "centering:byminimumR+ or centering:byminimum", "centering:bymeanR∓ or centering:bymean" , "centering:bymedianR∓ or centering:bymedian", "centering:bymodeR∓ or centering:bymode", "centering:bymaximumR∓ or centering:bymaximum", "centering:byminimumR∓ or centering:byminimum", "centering:bymeanR- or centering:bymean#", "centering:bymedianR- or centering:bymedian#", "centering:bymodeR- or centering:bymode#", "centering:bymaximumR- or centering:bymaximum#", "centering:byminimumR- or centering:byminimum#", "centering:never" or by a reference value' )
        
        # Ordering of data of the variable based on the input command
        if ordering == "ordering:ascend" or ordering == "ascend":
            data_ordered = sorted(data_centered)
        elif ordering == "ordering:descend" or ordering == "descend":
            data_ordered = sorted(data_centered)[::-1] 
        else:
            raise ValueError ('Invalid ordering command. Please, use "ordering:ascend", or "ordering:descend"') 
        data_1 = data_ordered
        
        # Establishing a suitable statistical mirror 
            # statistical meanic mirror
        if mirror_principal_value == "principal_value:mean" or mirror_principal_value == "mean":
            data_2 = [np.mean(data_ordered)] * len(data_ordered)
            # statistical medianic mirror
        elif mirror_principal_value == "principal_value:median" or mirror_principal_value == "median":
            data_2 = [np.median(data_ordered)] * len(data)
            # statistical modalic mirror
        elif mirror_principal_value == "principal_value:mode" or mirror_principal_value == "mode":
            data_2 = [statistics.mode(data)] * len(data_ordered)
            # statistical maximalic mirror
        elif mirror_principal_value == "principal_value:maximum" or mirror_principal_value == "maximum":
            data_2 = [np.max(data_ordered)] * len(data_ordered)
            # statistical minimalic mirror
        elif mirror_principal_value == "principal_value:minimum" or mirror_principal_value == "minimum":
            data_2 = [np.min(data_ordered)] * len(data_ordered)
            # statistical reference mirror on custom mode
        elif mirror_principal_value == "principal_value:reference_value" or mirror_principal_value == "reference_value":
            data_2 = [mirror_principal_value] * len(data_ordered)
            # statistical reference mirror
        elif isinstance(mirror_principal_value, (int, float)):
            data_2 = [mirror_principal_value] * len(data_ordered) 
        else:
            raise ValueError ('please, type any of "principal_value:mean", "principal_value:median", "principal_value:mode", "principal_value:minimum", "principal_value:maximum", "principal_value:reference value" or other refrence numerical value, of your choice as the principal value for mirror design')
            
        return data_1, data_2
        
    # Performing a customized preporocessing of the data prior to isomorphic optinalysis
    data_xy = preprocessing([data, mirror_principal_value, centering, ordering])
    
    # Extracting each from the two results after preprocessing transformations 
    data_x = data_xy[0] 
    data_y = data_xy[1] 
    
    ## Optinalytic model calculations stage: the isomorphic optinalysis between the preprocessed data and its designed statistical mirror
    # Perform Kabirian-based isomorphic analysis 
    outcomes = isomorphic_optinalysis_([data_x, data_y, pairing, print_result])

    # Return the outcome(s) estimate based on the chosen result to print. 
    return outcomes 


def doc_stat_mirroring():
    print("""
    Performs statistical dispersion estimations on a dataset using a parameterized, customized, and optimized Kabirian-based isomorphic optinalysis.

    Estimates statistical dispersion from a defined centre using customized centering, ordering, and other statistical mirroring principles. It is a parameterized and customized application of 
    Kabirian-based isomorphic optinalysis. It computes the Kabirian coefficient of proximity (kc), probability of proximity (pprox), probability of deviation (pdev), and alternate Kabirian coefficients (kc_alt1, kc_alt2). 
    This is based on the transformed dataset and its statistical mirror.

    The process of statistical mirroring comprises two distinct phases:
        a)	Preprocessing phase [Ref_1]: This involves applying preprocessing transformations, such as compulsory theoretical ordering, with or without centering the data. 
        It also encompasses tasks like statistical mirror design and optimizations within the established optinalytic construction. These optimizations include selecting an 
        efficient pairing style, central normalization, and establishing an isoreflective pair between the preprocessed data and its designed statistical mirror. 
        b)	Optinalytic model calculation phase [Ref_2]: This phase is focused on computing estimates (such as the Kabirian coefficient of proximity, 
        the probability of proximity, and the deviation) based on Kabirian-based isomorphic optinalysis models. 

    Args:
        instruction_list (list) : A list of instructions that includes the following six elements:
            - instruction_list[0] : array-like
                The dataset to be analyzed.
            - instruction_list[1] : str or numeric
                The principal value used for mirror design. Can be one of the following strings:
                * "principal_value:mean" or "mean"        : Here, the mean of the trnasformed data constructs the statistical mirror.
                * "principal_value:median" or "median"    : Here, the median of the trnasformed data constructs the statistical mirror.
                * "principal_value:mode" or "mode"        : Here, the mode of the trnasformed data constructs the statistical mirror.
                * "principal_value:maximum" or "maximum"  : Here, the maximum of the trnasformed data constructs the statistical mirror.
                * "principal_value:minimum" "minimum"     : Here, the minimum of the trnasformed data constructs the statistical mirror.
                * a custom numeric value                  : Here, the provided numeric value constructs the statistical mirror.
            - instruction_list[2] : str or numeric
                The centering method. Options include:
                * "centering:never"     : No centering applied.
                * "centering:bymean*", or "centering:bymeanR+"       : Center by mean and return absolute positive values.
                * "centering:bymedian*", or "centering:bymedianR+"   : Center by median and return absolute positive values.
                * "centering:bymode*", or "centering:bymodeR+"       : Center by mode and return absolute positive values.
                * "centering:bymaximum*", or "centering:bymaximumR+" : Center by maximum and return absolute positive values.
                * "centering:byminimum*", or "centering:byminimumR+" : Center by minimum and return absolute positive values.
                * "centering:bymean", or "centering:bymeanR∓"        : Center by mean without absolute values.
                * "centering:bymedian", or "centering:bymedianR∓"    : Center by median without absolute values.
                * "centering:bymode", or "centering:bymodeR∓"        : Center by mode without absolute values.
                * "centering:bymaximum", or "centering:bymaximumR∓"  : Center by maximum without absolute values.
                * "centering:byminimum", or "centering:byminimumR∓"  : Center by minimum without absolute values.
                * "centering:bymean#", or "centering:bymeanR-"       : Center by mean and return absolute negative values.
                * Custom numeric value for user-defined centering.
                    > Note: You can ignore the 'centering: ' word. For instance: "centering:never" as "never" in its specific order.
            - instruction_list[3] : str
                The ordering method. Options include:
                * "ordering:ascend" or "ascend"     : Sort data in ascending order.
                * "ordering:descend" or "descend"   : Sort data in descending order.
            - instruction_list[4] : str
                Pairing method for isomorphic optinalysis. Options include:
                * "pairing:H_H" or "H_H"    : For head-to-head (the lowest ends of the isoreflective pair of points are maximally distant).
                * "pairing:T_T" or "T_T"    : For tail-to-tail (the lowest ends of the isoreflective pair of points are minimally distant).
            - instruction_list[5] : str
                Specifies the result to return. Options include: 
                * "print:kc" or "kc"          : Prints Kabirian coefficient of proximity.
                * "print:pprox" or "pprox"    : Prints probability of proximity.
                * "print:pdev" or "pdev"      : Prints probability of deviation.
                * "print:kcalt1" or "kcalt1"  : Prints A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2"  : Prints D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"    : Prints the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises: 
        ValueError
            If invalid values are provided for centering, ordering, or the principal value for the mirror design.

    Examples:
        >>> import kbomodels as kbo
        >>> data = [-8.89, 47.91, 122.87, -3.02, -2.68, 60.17, 30.3, 113.62]

        >>> # Example 1: Absolute meanic mirroring (Scaloc-invariant estimation)
        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:bymean*", "ordering:ascend", "pairing:H_H", "print:kc"])
        0.9285721008593181

        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:bymean*", "ordering:ascend", "pairing:H_H", "print:pprox"])
        0.840709450595581

        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:bymean*", "ordering:ascend", "pairing:H_H", "print:pdev"])
        0.159290549404419

        >>> # Example 2: Raw meanic mirroring (Scale-invariant estimation)
        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:never", "ordering:ascend", "pairing:H_H", "print:kc"])
        0.8834145225095626

        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:never*", "ordering:ascend", "pairing:H_H", "print:pprox"])
        0.7414505643231742

        >>> kbo.stat_mirroring([data, "principal_value:mean", "centering:never*", "ordering:ascend", "pairing:H_H", "print:pdev"])
        0.25854943567682576

        >>> # Example 3: Raw maximalic mirroring
        >>> kbo.stat_mirroring([data, "principal_value:maximum", "centering:never", "ordering:ascend", "pairing:H_H", "print:kc"])
        0.7677090199694419

        >>> kbo.stat_mirroring([data, "principal_value:maximum", "centering:never", "ordering:ascend", "pairing:H_H", "print:pprox"])
        0.49209306975510636

        >>> kbo.stat_mirroring([data, "principal_value:maximum", "centering:never", "ordering:ascend", "pairing:H_H", "print:pdev"])
        0.5079069302448936

    Notes:
        This function performs three main steps:
        1. **Preprocessing**: The data is centered, ordered, and transformed according to the specified instructions.
        2. **Mirror Design**: A statistical mirror is established based on the principal value (mean, median, mode, maximum, minimun, or any other defined location estimate).
        3. **Optinalytic Model Calculation**: Kabirian-based Isomorphic optinalysis is applied between the preprocessed data and its statistical mirror to estimate the statistical dispersion.

        The Statistical Mirroring function is highly customizable, allowing users to define various centering methods, mirror designs, ordering, and pairing styles to meet their analysis needs. 
        For user-specific invariance tasks, the scaloc and scale invariance properties of the estimation outcomes are solely determined by the decision to apply or skip the centering process, respectively.
    
    Key Concepts:
            - **Kabirian coefficient of proximity (kc)**: A measure of the coefficient of dispersion from the defined center.
            - **Probability of proximity (pprox)**: The likelihood that data points are closely dispersed around a defined center.
            - **Probability of deviation (pdev)**: The likelihood that data points are distantly dispersed around a defined center.
            - **Alternate Kabirian coefficients**: The alternate Kabirian coefficients such as kcalt1, kcalt2, kcalt. 

    References:
        Cite these references to acknowledge the methodologies:
        [Ref_1] Abdullahi, K. B. (2024). Statistical mirroring: A robust method for statistical dispersion estimation. 
        MethodsX, 12, 102682. https://doi.org/10.1016/j.mex.2024.102682 
        
        [Ref_2] Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite this reference to acknowledge the Python code implementation of the methodology:
        [Ref_1] Abdullahi, K. B. (2024). A Python Code for statistical mirroring. Mendeley Data, V4. 
        doi: 10.17632/ppfvc65m2v.4 (https://data.mendeley.com/datasets/ppfvc65m2v/4)

        [Ref_2] Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)
    


# *****************************************************************************************************************************************************************
## Function for famispacing (family spacing) estimation using a customized, and optimized Kabirian-based isomorphic optinalysis
# *****************************************************************************************************************************************************************
def famispacing(instruction_list: list) -> any:
    """
    Estimates family spacing conformity and disconformity using a customized, and optimized Kabirian-based isomorphic optinalysis.
    
    This function calculates the conformity or disconformity of family spacing based on observed children's ages 
    and a specified birth-spacing interval. The calculation involves preprocessing input data, transforming observed children’s ages, 
    generating expected children ages, and applying the isomorphic optinalysis model to estimate key metrics like the Kabirian coefficient of conformity (kc), 
    probability of conformity (p-conform), and probability of disconformity (p-disconform).

    The process of famispacing estimation comprises two distinct phases:
        a)	Preprocessing phase **[Ref_1]**: This involves applying preprocessing operations and transformations, such parameters distillation, theoretical ordering 
        and shifts transformations with absolutely no data centering. It also encompasses tasks like conceptual age pattern generation and optimizations within the 
        established optinalytic construction. These optimizations include selecting an efficient pairing style, central normalization, and establishing an isoreflective pair 
        between the two preprocessed data. The data are the observed and expected patterns of biological children ages. 
        b)	Optinalytic model calculation phase **[Ref_2]**: This phase is focused on computing estimates (such as the Kabirian coefficient of conformity (similarity), 
        the probability of conformity (similarity), and the disconformity (dissimilarity)) based on Kabirian-based isomorphic optinalysis models.

    Args:
        instruction_list (list): A list of six elements containing the following:
            - observed_children_ages (list of float): Ages of observed biological children ever born alive (in months or years.months format).
            - parent_age (float): Age of the parent (in months or years.months format).
            - data_input_format (str): Format for the ages of children and parent, either 
                * "data_format:months" or "months"              : For ages recorded in months.
                * "data_format:years.months" or "years.months"  : For ages recorded in years.months (E.g., 9 years and 11 months of age becomes 9.11)
            - parent_status (str): Parent's status, option are:
                * "status:maternal" or "maternal"   : Indicating whether the calculation is for maternal family spacing.
                * "status:paternal" or "paternal"   : Indicating whether the calculation is for paternal family spacing.
            - spacing_interval_scheme (str or int): The birth-spacing interval scheme, option are:  
                * spacing_scheme:12 months" or "12 months"   : 12 months spacing between all births.
                * spacing_scheme:24 months" or "24 months"   : 24 months spacing between all births.
                * spacing_scheme:36 months" or "36 months"   : 36 months spacing between all births.
                * or a numeric value in months               : User-defined value in months spacing between for all births.
            - print_result (str): The type of result to print, including:
                * "print:kc" or "kc"                     : Prints the Kabirian coefficient of conformity.
                * "print:p-conform" or "p-conform"       : Prints the probability of conformity.
                * "print:p-disconform" or "p-disconform" : Prints the probability of disconformity.
                * "print:all_in_list" or "all_in_list"   : Pirnts all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"   : Prints all computed estimates in a dictionary.
    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If the input parent_age is less than the age of the first child, indicating an invalid data entry.

    Example:
        >>> import kbomodels as kbo
        >>> # Example data for children's ages in months and a 525-month-old maternal parent. Following 24-month spacing scheme, calculate the family spacing estimates.
        >>> data = [43, 86, 127, 172, 207, 249]
        >>> parent_age = 525
        >>> data_format = "months"
        >>> parent_status = "maternal" 
        >>> spacing_scheme = "24-month" 

        >>> # Estimate the Kabirian coefficient of conformity (kc).
        >>> kbo.famispacing([data, parent_age, data_format, parent_status, spacing_scheme, "print:kc"])
        1.064641580828253

        >>> # Estimate the probability of conformity.
        >>> kbo.famispacing([data, parent_age, data_format, parent_status, spacing_scheme, "print:p-conform"])
        0.867699257825105

        >>> # Estimate the probability of disconformity.
        >>> kbo.famispacing([data, parent_age, data_format, parent_status, spacing_scheme, "print:p-disconform"])
        0.13230074217489496

    **How It Works:**
        1. Converts the children's and parent's ages from "years.months" format to months if necessary.
        2. Verifies input data, ensuring the parent's age is not less than the first child's age and doesn't exceed the reproductive age limit (55 years for maternal and 70 years for paternal).
        3. Adjusts observed children’s ages based on the birth-spacing interval scheme.
        4. Generates expected children ages based on the birth-spacing interval.
        5. Applies shift transformations to account for age and fertility transition.
        6. Computes Kabirian-based isomorphic optinalysis estimates for family spacing conformity and disconformity.

    **Key Concepts:**
            - **Kabirian Coefficient of conformity (kc)**: A measure of the conformity or similarity between observed and expected children ages.
            - **Probability of Conformity (p-conform)**: The likelihood that observed children ages follow the specified spacing scheme.
            - **Probability of Disconformity (p-disconform)**: The likelihood of deviation from the specified spacing scheme.

    **References:**
        *Cite these references to acknowledge the methodologies:* 
        **[Ref_1]** Abdullahi, K.B., El-Sunais, Y.S., Yusuf, H., Kaware, M.S., Suleiman, M., Isah, M.B., Yar’adua, S.S., Kankara, S.S., Bello, A. (2024). 
        Famispacing: A Comprehensive and Sensitive Method for Family Spacing Estimation. Update the published citation details here.  
        
        **[Ref_2]** Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite these references to acknowledge the Python codes implementation of the methodologies:*
        **[Ref_1]** Abdullahi, K.B., El-Sunais, Y.S., Yusuf, H., Kaware, M.S., Suleiman, M., Isah, M.B., Yar’adua, S.S., Kankara, S.S., Bello, A. (2024). 
        A Python Code for Famispacing Estimation. Mendeley Data, V3. 
        doi: 10.17632/c3cfw72d4n.3 (https://data.mendeley.com/datasets/c3cfw72d4n/3)

        **[Ref_2]** Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    # Extract data from the instruction_list
    observed_children_ages_input = instruction_list[0]
    parent_age_input = instruction_list[1]
    data_input_format = instruction_list[2]
    parent_status = instruction_list[3]
    spacing_interval_scheme = instruction_list[4]
    print_result = instruction_list[5]

    # Function for performing isomorphic optinalysis
    def isomorphic_optinalysis_(instruction_list: list) -> any:
        # Extracting input data from the instruction_list
        data_x = instruction_list[0]  
        data_y = instruction_list[1] 
        pairing = instruction_list[2]  
        print_result = instruction_list[3] 
        
        # Calculating the kc estimate of the isomorphic optinalysis
        kc = kc_isoptinalysis(instruction_list)
        num_of_dimensions = len(data_x)
        
        # Calculating (translating) other estimates of isomorphic optinalysis based on the selected result(s) to be printed from the print_result input
        if print_result == "print:kc" or print_result == "kc":
            result = kc
        elif print_result == "print:p-conform" or print_result == "p-conform":
            p_conform_value = pSimSymId(kc, num_of_dimensions)
            result = p_conform_value
        elif print_result == "print:p-disconform" or print_result == "p-disconform":
            p_conform_value = pSimSymId(kc, num_of_dimensions)
            p_disconform_value = pDsimAsymUid(p_conform_value)
            result = p_disconform_value
        elif print_result == "print:all_in_list" or print_result == "all_in_list":
            p_conform_value = pSimSymId(kc, num_of_dimensions)
            p_disconform_value = pDsimAsymUid(p_conform_value)
            result = [
            kc,
            p_conform_value,
            p_disconform_value
            ]
        elif print_result == "print:all_in_dict" or print_result == "all_in_dict":
            p_conform_value = pSimSymId(kc, num_of_dimensions)
            p_disconform_value = pDsimAsymUid(p_conform_value)
            result = {
            "kc": kc,
            "p-conform": p_conform_value,
            "p-disconform": p_disconform_value
            }
        else:
            raise ValueError('Invalid print_result command. Please, use "print:kc", "print:p-conform", "print:p-disconform",  "print:all_in_list, or "print:all_in_dict" ')
        return result

    # convert children ages and parent's age in years to months if not provided in months
    # This function 'convert_ages' do this task
    def convert_age(age):
        part = str(age).split('.')
        age_years = int(part[0])
        age_months = int(part[1])
        converted_age = (age_years * 12) + age_months
        return converted_age

    if data_input_format == "years.months" or data_input_format == "data_format:years.months":
         observed_children_ages = [convert_age(i) for i in observed_children_ages_input]
         parent_age = convert_age(parent_age_input)
    elif data_input_format == "months" or data_input_format == "data_format:months":
         observed_children_ages = observed_children_ages_input
         parent_age = parent_age_input

    # Defining, checking and verifying some important feature ages and parameters
    menopausal_infertility_age = 660    # 660 months, equivalent to 55 years, is used. User can change this value depemding on the reference to be used.
    andropausal_infertility_age = 840   # 840 months, equivalent to 70 years, is used. User can change this value depemding on the reference to be used.
    children_number = len(observed_children_ages_input)
    first_child_age = np.max(observed_children_ages_input)

        # Check, verify and correct the consistency of data input
    if parent_age_input < first_child_age:
        raise ValueError ("Invalid data entry: Do you mean a child is older than his/her parent. Please, enter the valid ages.")

        # Check if parent_status as maternal or paternal form the input list. 
    if parent_status == "maternal" or parent_status == "status:maternal":
        reproductive_infertility_age = menopausal_infertility_age
    elif parent_status == "paternal" or parent_status == "status:paternal":
        reproductive_infertility_age = andropausal_infertility_age

        # Check if parent_age does not exceeds the reproductive infertility age 
    if parent_age > reproductive_infertility_age:
        parent_age1 = reproductive_infertility_age
    else:
        parent_age1 = parent_age

        # Calculate the future fertility based on the parent's age and the assumed reproductuve infertility age
    future_fertility_age = reproductive_infertility_age - parent_age1 

    # Check what is chosen/provided as the birth-spacing interval scheme form the input list. 
    if spacing_interval_scheme == "12 months" or spacing_interval_scheme == "spacing_scheme:12 months":
        spacing_interval_schemex = 12
    elif spacing_interval_scheme == "24 months" or spacing_interval_scheme == "spacing_scheme:24 months":
        spacing_interval_schemex = 24
    elif spacing_interval_scheme == "36 months" or spacing_interval_scheme == "spacing_scheme:36 months":
        spacing_interval_schemex = 36
    else:
        spacing_interval_schemex = spacing_interval_scheme

    # Ordering transformation: Arrange the observed_children_ages in ascending order 
    transformed1_observed_children_ages = sorted(observed_children_ages)
    
    # Shift transformation: aim to adjust the ages based on the last born child and the birth-spacing interval scheme chosen.
    # Check if each element in the list is less than or greater than to the birth-spacing_interval_scheme and then shift transform the ages
        # This is the function for shift transformation
    def modify_ages(age_list, spacing_interval):
        # Check the first element of the list
        if age_list[0] != spacing_interval:
            shift_value = spacing_interval - age_list[0]
            m_list = [age + shift_value for age in age_list]
        else:
            m_list = age_list
        # Return the shifted elements of the list
        return m_list
    
    transformed2_observed_children_ages = modify_ages( transformed1_observed_children_ages, spacing_interval_schemex)

    # Generate the expected children ages
    def generate_expected_children_ages(start, interval, length):
        """
        - start is the birth-spacing interval scheme,
        - interval is the birth-spacing interval scheme, and 
        - length is the number of observed children ever born alive.
        """
        # Use list comprehension to generate the list
        result_list = [start + i * interval for i in range(length)]
        return result_list
    expected_children_ages = generate_expected_children_ages(transformed2_observed_children_ages[0], spacing_interval_schemex, children_number)

    # Shift transformation: aim to mitigate/balance the effect of age and fertility transition 
    if parent_age <= reproductive_infertility_age:
        transformed3_observed_children_ages = [future_fertility_age + age for age in transformed2_observed_children_ages]
        transformed3_expected_children_ages = [future_fertility_age + age for age in expected_children_ages]
    else:
        transformed3_observed_children_ages = [future_fertility_age - age for age in transformed2_observed_children_ages]
        transformed3_expected_children_ages = [future_fertility_age - age for age in expected_children_ages]
        
    # Kabirian-based isomorphic optinalysis model calculations.
    # The arrangement and restricted rotation of function "optinalysis (observed_data, expected_data)" is respected to ensure consistent order of interpretation of the kc-estimate. 
    outcome = isomorphic_optinalysis_([transformed3_observed_children_ages, transformed3_expected_children_ages, "pairing:T_T", print_result])
    
    # Return the outcome(s) estimate based on the chosen result to print. 
    return outcome


def doc_famispacing():
    print("""
    Estimates family spacing conformity and disconformity using a customized, and optimized Kabirian-based isomorphic optinalysis.
    
    This function calculates the conformity or disconformity of family spacing based on observed children's ages 
    and a specified birth-spacing interval. The calculation involves preprocessing input data, transforming observed children’s ages, 
    generating expected children ages, and applying the isomorphic optinalysis model to estimate key metrics like the Kabirian coefficient of conformity (kc), 
    probability of conformity (p-conform), and probability of disconformity (p-disconform).

    The process of famispacing estimation comprises two distinct phases:
        a)	Preprocessing phase [Ref_1]: This involves applying preprocessing operations and transformations, such parameters distillation, theoretical ordering 
        and shifts transformations with absolutely no data centering. It also encompasses tasks like conceptual age pattern generation and optimizations within the 
        established optinalytic construction. These optimizations include selecting an efficient pairing style, central normalization, and establishing an isoreflective pair 
        between the two preprocessed data. The data are the observed and expected patterns of biological children ages. 
        b)	Optinalytic model calculation phase [Ref_2]: This phase is focused on computing estimates (such as the Kabirian coefficient of conformity (similarity), 
        the probability of conformity (similarity), and the disconformity (dissimilarity)) based on Kabirian-based isomorphic optinalysis models.

    Args:
        instruction_list (list): A list of six elements containing the following:
            - observed_children_ages (list of float): Ages of observed biological children ever born alive (in months or years.months format).
            - parent_age (float): Age of the parent (in months or years.months format).
            - data_input_format (str): Format for the ages of children and parent, either 
                * "data_format:months" or "months"              : For ages recorded in months.
                * "data_format:years.months" or "years.months"  : For ages recorded in years.months (E.g., 9 years and 11 months of age becomes 9.11)
            - parent_status (str): Parent's status, option are:
                * "status:maternal" or "maternal"   : Indicating whether the calculation is for maternal family spacing.
                * "status:paternal" or "paternal"   : Indicating whether the calculation is for paternal family spacing.
            - spacing_interval_scheme (str or int): The birth-spacing interval scheme, option are:  
                * spacing_scheme:12 months" or "12 months"   : 12 months spacing between all births.
                * spacing_scheme:24 months" or "24 months"   : 24 months spacing between all births.
                * spacing_scheme:36 months" or "36 months"   : 36 months spacing between all births.
                * or a numeric value in months               : User-defined value in months spacing between for all births.
            - print_result (str): The type of result to print, including:
                * "print:kc" or "kc"                     : Prints the Kabirian coefficient of conformity.
                * "print:p-conform" or "p-conform"       : Prints the probability of conformity.
                * "print:p-disconform" or "p-disconform" : Prints the probability of disconformity.
                * "print:all_in_list" or "all_in_list"   : Pirnts all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"   : Prints all computed estimates in a dictionary.
    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If the input parent_age is less than the age of the first child, indicating an invalid data entry.

    Example:
        >>> import kbomodels as kbo
        >>> # Example data for children's ages in months and a 525-month-old maternal parent. Following 24-month spacing scheme, calculate the family spacing estimates.
        >>> data = [43, 86, 127, 172, 207, 249]
        >>> parent_age = 525
        >>> data_format = "months"
        >>> parent_status = "maternal" 
        >>> spacing_scheme = "24-month" 

        >>> # Estimate the Kabirian coefficient of conformity (kc).
        >>> kbo.famispacing([data, parent_age, data_format, parent_status, spacing_scheme, "print:kc"])
        1.064641580828253

        >>> # Estimate the probability of conformity.
        >>> kbo.famispacing([data, parent_age, data_format, parent_status, spacing_scheme, "print:p-conform"])
        0.867699257825105

        >>> # Estimate the probability of disconformity.
        >>> kbo.famispacing([data, parent_age, data_format, parent_status, spacing_scheme, "print:p-disconform"])
        0.13230074217489496

    How It Works:
        1. Converts the children's and parent's ages from "years.months" format to months if necessary.
        2. Verifies input data, ensuring the parent's age is not less than the first child's age and doesn't exceed the reproductive age limit (55 years for maternal and 70 years for paternal).
        3. Adjusts observed children’s ages based on the birth-spacing interval scheme.
        4. Generates expected children ages based on the birth-spacing interval.
        5. Applies shift transformations to account for age and fertility transition.
        6. Computes Kabirian-based isomorphic optinalysis estimates for family spacing conformity and disconformity.

    Key Concepts:
            - **Kabirian Coefficient of conformity (kc)**: A measure of the conformity or similarity between observed and expected children ages.
            - **Probability of Conformity (p-conform)**: The likelihood that observed children ages follow the specified spacing scheme.
            - **Probability of Disconformity (p-disconform)**: The likelihood of deviation from the specified spacing scheme.

    References:
        Cite these references to acknowledge the methodologies:
        [Ref_1] Abdullahi, K. B., El-Sunais, Y.S., Yusuf, H., Kaware, M. S., Suleiman, M., Isah, M. B., Yar’adua, S. S., Kankara, S. S., Bello, A. (2024). 
        Famispacing: A Comprehensive and Sensitive Method for Family Spacing Estimation. Update the published citation details here.  
        
        [Ref_2] Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite these references to acknowledge the Python codes implementation of the methodologies:
        [Ref_1] Abdullahi, K. B., El-Sunais, Y. S., Yusuf, H., Kaware, M. S., Suleiman, M., Isah, M. B., Yar’adua, S. S., Kankara, S. S., Bello, A. (2024). 
        A Python Code for Famispacing Estimation. Mendeley Data, V3. 
        doi: 10.17632/c3cfw72d4n.3 (https://data.mendeley.com/datasets/c3cfw72d4n/3)

        [Ref_2] Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)



# *****************************************************************************************************************************************************************
## SM-based ordinalysis is a function for calculating an individual's level of assessments on a defined points ordinal scales 
# *****************************************************************************************************************************************************************
def smb_ordinalysis(input_list: list) -> any:
    """
    Perform statistical mirroring-based ordinalysis (SM-based ordinalysis), a descriptive methodology for assessing an individual's level of 
    assessments on a defined ordinal scale by applying a customized and optimized statistical mirroring techniques.

    The Statistical Mirroring-based Ordinalysis process consists of three distinct phases: 
        a) Adaptive Customization and Optimization Phase [Ref_1]: This phase forms the foundation of the methodology. 
        It involves adaptively customizing and optimizing parameters to meet the specific requirements of the statistical mirroring estimation for the given task.
        b) Statistical Mirroring Analysis Phase [Ref_2]: In this phase, the appropriate type of statistical mirroring is applied, as determined by the customizations made in phase one.
        c) Optinalytic Model Calculation Phase [Ref_3]: This phase focuses on calculating estimates, such as the Kabirian coefficient of proximity, probability of proximity, 
        and deviation, using Kabirian-based isomorphic optinalysis models.

    Args:
        input_list (list): A list containing the following elements:
            - data (list): A list of ordinal data representing the individual's assessments on a defined point scale.
            - point_scale (int): The n-point ordinal scale (e.g.: 5 for a 5-point Likert/rating scale, and 7 for a 7-point Likert/rating scale).
            - max_scale (int): The maximum value on the ordinal scale (e.g., 5 for a 5-point Likert/rating scale with a common interval of 1, and 10 for a 5-point Likert/rating scale with a common interval of 2).
            - encoding (str): Specifies whether the values are on natural or real coding or encoding structure. Options can include:
                * "encoding:natural_numbers" or "natural_numbers"       : Means the values are on natural number coding or encoding structure.
                * "encoding:whole_numbers" or "encoding:whole_numbers"  : Means the values are on whole number coding or encoding structure.
            - print_result (str): Specifies which type of result(s) to print or return. Options can include:
                * "print:kc-sprox" or "kc-sprox"    : Prints Kabirian coefficient of positive assessment.
                * "print:p-sprox" or "p-sprox"      : Prints probability of positive assessment.
                * "print:p-sdev" or "p-sdev"        : Prints probability of negative assessment.
                * "print:kcalt1" or "kcalt1" : Prints A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2" : Prints D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"   : Prints the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If the input data is not properly formatted or does not match the expected structure.

    Example:
        >>> import kbomodels as kbo
        >>> # Example data and analysis on a 5-point scale on ordinal (natural numbers) encoding, with 5 value encoded as strongly agreed response.
            >>> data = [4, 3, 1, 4, 4]
            >>> point_scale = 5
            >>> max_scale = 5
            >>> encoding = "natural_numbers"
            >>> kbo.smb_ordinalysis([data, point_scale, max_scale, encoding, "print:all_in_dict"])
            # Outcomes
            {'kc-sprox': 0.8454545454545456,
            'p-sprox': 0.6402116402116403,
            'p-sdev': 0.35978835978835966,
            'kc_alt1': 0.8454545454545455,
            'kc_alt2': 1.2236842105263155,
            'kc_alt': 1.2236842105263155}

    Process Overview:
        1. Input Data Extraction:
            - The function extracts the input ordinal data, the n-point_scale, the maximum value of the scale, 
            the encoding structure, and the desired output format (print_result) from the provided `input_list`.

        2. Statistical Mirroring:
            - The function applies statistical mirroring, a method that orders and pairs
            ordinal data for analysis. The specific mirroring setup in this function uses:
                - "centering:never" (no centering of the data),
                - "ordering:ascend" (data is ordered in ascending fashion),
                - "pairing:H_H" (the lowest ends of the isoreflective pair of points are maximally distant).
        
        3. Customized Output:
            - Based on the `print_result` parameter, the function customizes the returned results.
            The user can request only mirrored data or all computed statistics.

    Notes:
            - This function relies on the `stat_mirroring` function, which implements the core 
            statistical mirroring function for ordinal data. Ensure the `stat_mirroring` function 
            is properly imported and defined in the same context.
            - The statistical mirroring methodology used in this function is highly customizable 
            and adaptable for various point scales and assessment types.

    References:
        Cite these references to acknowledge the methodologies:
        **[Ref_1]** Abdullahi, K. B. (2024). Statistical Mirroring-based ordinalysis: A sensitive, robust, and efficient 
        methodology for analysis of ordinal assessments data. Update the published citation details here.

        [Ref_2] Abdullahi, K. B. (2024). Statistical mirroring: A robust method for statistical dispersion estimation. 
        MethodsX, 12, 102682. https://doi.org/10.1016/j.mex.2024.102682 
        
        [Ref_3] Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite these references to acknowledge the Python codes implementation of the methodologies:
        [Ref_1] Abdullahi, K. B. (2024). Python Code for Statistical Mirroring-based Ordinalysis. 
        Mendeley Data, V1. doi: 10.17632/x45wvbd3sv.1 (https://data.mendeley.com/datasets/x45wvbd3sv/1) 

        [Ref_2] Abdullahi, K. B. (2024). A Python Code for statistical mirroring. Mendeley Data, V4. 
        doi: 10.17632/ppfvc65m2v.4 (https://data.mendeley.com/datasets/ppfvc65m2v/4)

        [Ref_3] Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3)           
    """

    # Extracting data from the input_list
    data = input_list[0]
    point_scale = input_list[1]
    max_scale = input_list[2]
    encoding = input_list[3]
    print_result = input_list[4]

    if encoding == "encoding:natural_numbers" or encoding == "natural_numbers" or encoding == "NN":
        scale_interval = max_scale / point_scale        # ordinal (natural number) coding or encoding assumes equal interval
        encoded_max_scale = max_scale - scale_interval
        encoded_data = [item - scale_interval for item in data]
    elif encoding == "encoding:whole_numbers" or encoding == "whole_numbers" or encoding == "WN":
        encoded_max_scale = max_scale
        encoded_data = data
    else:
        raise ValueError ('Invalid data selection: Use "encoding:natural_numbers" or "natural_numbers" or "NN". Else, use "encoding:whole_numbers" or "whole_numbers" or "WN" for whole number encoding') 

    # Customized and optimized statistical analysis using statistical mirroring. The setting of the parameters is based on the described methodology of smb-ordinalysis  
    results = stat_mirroring([encoded_data, encoded_max_scale, "centering:never", "ordering:ascend", "pairing:H_H", "print:all_in_list"]) 

    # Printing the exposuremetrics estimates based on the provided print input command
    if print_result in {"print:kc", "kc", "print:kc-sprox", "kc-sprox"}:
        return results[0]
    elif print_result in {"print:pprox", "pprox", "print:p-sprox", "p-sprox"}:
        return results[1]
    elif print_result in {"print:pdev", "pdev", "print:p-sdev", "p-sdev"}:
        return results[2]
    elif print_result in {"print:kcalt1", "kcalt1"}:
        return results[3]
    elif print_result in {"print:kcalt2", "kcalt2"}:
        return results[4]
    elif print_result in {"print:kcalt", "kcalt"}:
        return results[5]
    elif print_result in {"print:all_in_list", "all_in_list"}:
        return [
                results[0],
                results[1],
                results[2],
                results[3],
                results[4],
                results[5]
                ]
    elif print_result == "print:all_in_dict" or print_result == "all_in_dict":
        return {
                "kc-sprox": results[0],
                "p-sprox": results[1],
                "p-sdev": results[2],
                "kcalt1": results[3],
                "kcalt2": results[4],
                "kcalt": results[5]
                }
    else:
        raise ValueError('Invalid print_result format. Use one of: "kc-sprox" or "kc", "p-sprox" or "pprox", "p-sdev" or "pdev", "kcalt1", "kcalt2", "kcalt", all_in_list", "all_in_dict" ')
    

def doc_smb_ordinalysis():
    print("""
    Perform statistical mirroring-based ordinalysis (SM-based ordinalysis), a descriptive methodology for assessing an individual's level of 
    assessments on a defined ordinal scale by applying a customized and optimized statistical mirroring techniques.

    The Statistical Mirroring-based Ordinalysis process consists of three distinct phases: 
        a) Adaptive Customization and Optimization Phase [Ref_1]: This phase forms the foundation of the methodology. 
        It involves adaptively customizing and optimizing parameters to meet the specific requirements of the statistical mirroring estimation for the given task.
        b) Statistical Mirroring Analysis Phase [Ref_2]: In this phase, the appropriate type of statistical mirroring is applied, as determined by the customizations made in phase one.
        c) Optinalytic Model Calculation Phase [Ref_3]: This phase focuses on calculating estimates, such as the Kabirian coefficient of proximity, probability of proximity, 
        and deviation, using Kabirian-based isomorphic optinalysis models.

    Args:
        input_list (list): A list containing the following elements:
            - data (list): A list of ordinal data representing the individual's assessments on a defined point scale.
            - point_scale (int): The n-point ordinal scale (e.g.: 5 for a 5-point Likert/rating scale, and 7 for a 7-point Likert/rating scale).
            - max_scale (int): The maximum value on the ordinal scale (e.g., 5 for a 5-point Likert/rating scale with a common interval of 1, and 10 for a 5-point Likert/rating scale with a common interval of 2).
            - encoding (str): Specifies whether the values are on natural or real coding or encoding structure. Options can include:
                * "encoding:natural_numbers" or "natural_numbers"       : Means the values are on natural number coding or encoding structure.
                * "encoding:whole_numbers" or "encoding:whole_numbers"  : Means the values are on whole number coding or encoding structure.
            - print_result (str): Specifies which type of result(s) to print or return. Options can include:
                * "print:kc-sprox" or "kc-sprox"    : Prints Kabirian coefficient of positive assessment.
                * "print:p-sprox" or "p-sprox"      : Prints probability of positive assessment.
                * "print:p-sdev" or "p-sdev"        : Prints probability of negative assessment.
                * "print:kcalt1" or "kcalt1" : Prints A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2" : Prints D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"   : Prints the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, or dict - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate.

    Raises:
        ValueError: If the input data is not properly formatted or does not match the expected structure.

    Example:
        >>> import kbomodels as kbo
        >>> # Example data and analysis on a 5-point scale on ordinal (natural numbers) encoding, with 5 value encoded as strongly agreed response.
            >>> data = [4, 3, 1, 4, 4]
            >>> point_scale = 5
            >>> max_scale = 5
            >>> encoding = "natural_numbers"
            >>> kbo.smb_ordinalysis([data, point_scale, max_scale, encoding, "print:all_in_dict"])
            # Outcomes
            {'kc-sprox': 0.8454545454545456,
            'p-sprox': 0.6402116402116403,
            'p-sdev': 0.35978835978835966,
            'kc_alt1': 0.8454545454545455,
            'kc_alt2': 1.2236842105263155,
            'kc_alt': 1.2236842105263155}

    Process Overview:
        1. Input Data Extraction:
            - The function extracts the input ordinal data, the n-point_scale, the maximum value of the scale, 
            the encoding structure, and the desired output format (print_result) from the provided `input_list`.

        2. Statistical Mirroring:
            - The function applies statistical mirroring, a method that orders and pairs
            ordinal data for analysis. The specific mirroring setup in this function uses:
                - "centering:never" (no centering of the data),
                - "ordering:ascend" (data is ordered in ascending fashion),
                - "pairing:H_H" (the lowest ends of the isoreflective pair of points are maximally distant).
        
        3. Customized Output:
            - Based on the `print_result` parameter, the function customizes the returned results.
            The user can request only mirrored data or all computed statistics.

    Notes:
            - This function relies on the `stat_mirroring` function, which implements the core 
            statistical mirroring function for ordinal data. Ensure the `stat_mirroring` function 
            is properly imported and defined in the same context.
            - The statistical mirroring methodology used in this function is highly customizable 
            and adaptable for various point scales and assessment types.

    References:
        Cite these references to acknowledge the methodologies:
        **[Ref_1]** Abdullahi, K. B. (2024). Statistical Mirroring-based ordinalysis: A sensitive, robust, and efficient 
        methodology for analysis of ordinal assessments data. Update the published citation details here.

        [Ref_2] Abdullahi, K. B. (2024). Statistical mirroring: A robust method for statistical dispersion estimation. 
        MethodsX, 12, 102682. https://doi.org/10.1016/j.mex.2024.102682 
        
        [Ref_3] Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 
        
        Cite these references to acknowledge the Python codes implementation of the methodologies:
        [Ref_1] Abdullahi, K. B. (2024). Python Code for Statistical Mirroring-based Ordinalysis. 
        Mendeley Data, V1. doi: 10.17632/x45wvbd3sv.1 (https://data.mendeley.com/datasets/x45wvbd3sv/1) 

        [Ref_2] Abdullahi, K. B. (2024). A Python Code for statistical mirroring. Mendeley Data, V4. 
        doi: 10.17632/ppfvc65m2v.4 (https://data.mendeley.com/datasets/ppfvc65m2v/4)

        [Ref_3] Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3)           
    """)



# *************************************************************************************************
## Qualitative exposuremetrics is a function for analyzing organismal resistance and susceptibility dynamics using qualitative variables.
# *************************************************************************************************
def qualitative_exposuremetrics(instruction_list):
    from kbomodels import stat_mirroring, kc_alt1, kc_alt2
    """
    Qualitative exposuremetrics is a measure of the biological proximity or deviation of an organism from the observed
    progressive threat or anti-threat responses to the expected cumulative threat or anti-threat responses (i.e., the residual,
    net, or gross expectation) as a result of exposure to a harmful agent(s). It estimates the organismal threat or
    anti-threat response dynamics of resistance and susceptibility within a population over successful events and generations.

    The organismal resistance is defined as the isoreflectivity (isoreflective pairing) of observed anti-threat
    responses to the expected cumulative anti-threat responses (i.e., the residual, net, or gross expectation).
    While organismal susceptibility is the deviation from attaining a complete and total resistance status.

    The process of exposuremetrics comprises four distinct phases:
            a)	Preprocessing (conceptualization, parameterization, adaptive customization and optimization) phase: This 
            phase forms the core of the methodology, defining key concepts and expectations derived from observed variables 
            to guide the design of the statistical mirror. It also involves customizing and optimizing parameters to ensure 
            the statistical mirroring process is well-suited to the specific analytical task.
            b)	Statistical Mirroring Analysis Phase **[Ref_2]**: This involves applying a suitable statistical mirroring type based on the 
            phase 1 adaption of the established adaptive customization and optimization of statistical mirroring parameters. 
            c)	Kabirian-based Optinalysis Model Calculation Phase **[Ref_3]**: This phase is focused on computing estimates 
            (such as the Kabirian coefficient of proximity, the probability of proximity, and the deviation) based on 
            Kabirian-based isomorphic optinalysis models. 
            d)  Advanced Exposuremetrics Calculations Phase **[Ref_1]**: These advanced metrics are the simple arithmetic differences 
            between qualitative exposuremetrics estimates.
    
    Args:
        input_list (list): A list containing the following 7 elements:
            - progressive threat or anti-threat responses (list): A list of responses at different exposure levels. E.g., mortality scores, 
            knockdown counts over periods during exposure.
            - net cumulative threat or anti-threat response (int, str): Observed cumulative threat or anti-threat response at a 
            specific period after exposure. 
            - gross cumulative threat or anti-threat response (int, str or "None"): Observed cumulative threat or anti-threat response from 
            a reference threshold (e.g., response due to synergist, or elicitor) at a specific period after exposure.
                * Note: These inputs (net and gross cumulative threat or anti-threat responses) are not neceaasary if the organisms were not 
                subjected to post-exposure treatment or others, you can write any non-numerical input (e.g., "Nil", "None", "Not recorded", e.t.c). 
                * However, you would not be able to calculate net or gross resistance and susceptibility estimates. 
            - population tested (int): The number of organisms tested or exposed.
            - data type (str): The number of organisms tested or exposed. Options can include one of:
                * "data_type:threat" or "threat", "data_type:mortality" or "mortality"           : For threat responses frequency.
                * "data_type:anti-threat" or "anti-threat", "data_type:survival" or "survival"   : For anti-threat responses frequency.
            - estimation method (str): The specific type of exposuremetrics analysis to compute. Options can include:
                * "method:residual" or "residual"   : Estimates residual resistance and susceptibility.
                * "method:net" or "net"             : Estimates net resistance and susceptibility.
                * "method:gross" or "gross"         : Estimates gross resistance and susceptibility.
                * "method:super residual" or "super residual"   : Estimates super residual resistance and susceptibility.
                * "method:super net" or "super net"             : Estimates super net resistance and susceptibility.
                * "method:super resnet" or "super resnet"       : Estimates super resnet resistance and susceptibility.
            - print_result (str): Specifies which type of result(s) to print or return. Options can include:
                * "print:kc-resistance" or "kc-resistance"           : Prints Kabirian coefficient of resistance.
                * "print:p-resistance" or "p-resistance"             : Prints probability of resistance.
                * "print:p-susceptibility" or "p-susceptibility"     : Prints probability of susceptibility.
                * "print:kcalt1" or "kcalt1" : Prints A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2" : Prints D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"   : Prints the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, dict, or str - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate. If not suitable data, some estimates may return a string 'NaN'.

    Raises:
        ValueError: If the input data is not properly formatted or does not match the expected structure.

    Example:
        >>> import kbomodels as kbo
        
        # Parameters and input data
        >>> progressive_threat_responses = [0, 2, 7, 10, 12]   # Mortality counts/frequency in five (5) interval periods of repeating observations.  
        >>> net_cumulative_threat_response = 19               # If the value is not obtained, write any non-numerical input e.g: "None", "No record", e.t.c.
        >>> gross_cumulative_threat_response = 22             # If the value is not obtained, write any non-numerical input e.g: "None", "No record", e.t.c.
        >>> population_tested = 25
        >>> data_type = "threat"       # Because the recorded response data is the threat, therefore it will be checked converted in the computation process. 
        >>> estimation_method_1 = "residual"
        >>> estimation_method_2 = "net"
        >>> estimation_method_3 = "gross"
        >>> estimation_method_4 = "super residual"
        >>> print_outcomes = "print:all_in_dict"
        
        # Calculating the estimates
        >>> print(f" Residual estimates = {kbo.qualitative_exposuremetrics([progressive_threat_responses, net_cumulative_threat_response, gross_cumulative_threat_response, population_tested, data_type, estimation_method_1, print_outcomes])} ")
        >>> print(f" Net estimates = {kbo.qualitative_exposuremetrics([progressive_threat_responses, net_cumulative_threat_response, gross_cumulative_threat_response, population_tested, data_type, estimation_method_2, print_outcomes])} ")
        >>> print(f" Gross estimates = {kbo.qualitative_exposuremetrics([progressive_threat_responses, net_cumulative_threat_response, gross_cumulative_threat_response, population_tested, data_type, estimation_method_3, print_outcomes])} ")
        >>> print(f" Super residual estimates = {kbo.qualitative_exposuremetrics([progressive_threat_responses, net_cumulative_threat_response, gross_cumulative_threat_response, population_tested, data_type, estimation_method_4, print_outcomes])} ")
        
        # Outcomes
        Residual estimates = {'kc-resistance': 1.1425149700598805, 'p-resistance': 0.7396061269146605, 'p-susceptibility': 0.26039387308533946, 'kcalt1': 0.8890959925442683, 'kcalt2': 1.1425149700598807, 'kcalt': 0.8890959925442683} 
        
        Net estimates = {'kc-resistance': 1.4307692307692308, 'p-resistance': 0.46919431279620843, 'p-susceptibility': 0.5308056872037916, 'kcalt1': 0.7685950413223139, 'kcalt2': 1.4307692307692308, 'kcalt': 0.7685950413223139} 
        
        Gross estimates = {'kc-resistance': 1.6987012987012986, 'p-resistance': 0.33906633906633915, 'p-susceptibility': 0.6609336609336609, 'kcalt1': 0.7085590465872156, 'kcalt2': 1.6987012987012984, 'kcalt': 0.7085590465872156} 
        
        Super residual estimates = {'kc-resistance': 2.7888238618404055, 'p-resistance': 0.13012797372986928, 'p-susceptibility': -0.13012797372986928, 'kcalt1': 0.6092264040794205, 'kcalt2': 2.7888238618404055, 'kcalt': 0.6092264040794205} 

    **Process Overview:**
        1. Input Data Extraction and Formatting:
            - The function extracts the inputs: progressive threat or anti-threat responses, net cumulative threat or 
            anti-threat response, gross cumulative threat or anti-threat response, population tested, data type, method, 
            and the desired output format (print_result) from the provided `input_list`.

        2. Statistical Mirroring:
            - The function applies Kabirian-based isomorphic optinalysis, and statistical mirroring methodology, a method that preprocessed,
            orders, and pairs input numerical data for analysis. The specific mirroring setup in this function uses:
                * "centering:never" (no centering of the data),
                * "ordering:ascend" (data is ordered in descending order),
                * "pairing:H_H" (the lowest ends of the isoreflective pair of points are maximally distant).
        
        3. Advance Exposuremetrics Analysis:
            - These advanced metrics are the simple arithmetic differences between the qualitative exposuremetrics estimates. 
        
        4. Customized Output:
            - Based on the `print_result` parameter, the function customizes the returned results.
            The user can request print only a specific result or all computed statistics.

    **Notes:**
            - This function relies on the `Kabirian-based isomorphic optinalysis`, and `statistical mirroring` function, which implements the core 
            qualitative exposuremetrics function for exposuremetrics data analysis of qualitative variable. 
            - Ensure the `statistical mirroring` and
            `D-alternative Kabirian coefficient (kcalt2)` functions are properly imported and defined in the same context.

    **References:**
        *Cite these references to acknowledge the methodologies:* 
        **[Ref_1]** Abdullahi, K. B.; Suleiman, M.; Wagini, N. H.; Sani, I. (2025). qualitative exposuremetrics: A comprehensive and sensitive estimation
        framework for analyzing organismal resistance and susceptibility dynamics using qualitative variables. 
        [You can follow updates for the published citation details].

        **[Ref_2]** Abdullahi, K. B. (2024). Statistical mirroring: A robust method for statistical dispersion estimation. 
        MethodsX, 12, 102682. https://doi.org/10.1016/j.mex.2024.102682 
        
        **[Ref_3]** Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite these references to acknowledge the Python codes implementation of the methodologies:*
        **[Ref_1]** Abdullahi, K. B. (2025). Python code for qualitative exposuremetrics analysis.
        Mendeley Data, V1. doi: 10.17632/xk38tj5vbw.1 (https://data.mendeley.com/datasets/xk38tj5vbw/1) 

        **[Ref_2]** Abdullahi, K. B. (2024). A Python code for statistical mirroring. Mendeley Data, V4. 
        doi: 10.17632/ppfvc65m2v.4 (https://data.mendeley.com/datasets/ppfvc65m2v/4)

        **[Ref_3]** Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """
    
    # Keys: TARs --- threat or anti-threat responses
    #       TAR --- Threat or anti-threat response
    #       ARs --- Anti-threat responses

    # Extract data from the instruction_list
    progressive_TARs_data = instruction_list[0]
    net_cumulative_TAR_data = instruction_list[1]
    gross_cumulative_TAR_data = instruction_list[2]
    population_tested = instruction_list[3]   # Number of organisms tested
    data_type = instruction_list[4]
    method = instruction_list[5]
    print_result = instruction_list[6]

    # Guard clause for input length to ensure instruction_list has exactly 7 elements
    if len(instruction_list) != 7:
        raise ValueError("instruction_list must contain exactly 7 elements.")
    
    # Validating inputs, and converting progressive and cumulative threat responses (data) to anti-threat responses.
        # Inputs are only valid and meets the qualitative exposuremetrics requirements if in anti-threat responses.
    def calculate_cumulative_ARs_data():
        """Helper function to calculate cumulative threat responses."""
        if not isinstance(net_cumulative_TAR_data, (int, float)) and not isinstance(gross_cumulative_TAR_data, (int, float)):
            return [int(i) for i in (population_tested - np.array(progressive_TARs_data))], "None", "None"
        elif not isinstance(net_cumulative_TAR_data, (int, float)):
            return [int(i) for i in (population_tested - np.array(progressive_TARs_data))], "None", int(population_tested - gross_cumulative_TAR_data)
        elif not isinstance(gross_cumulative_TAR_data, (int, float)):
            return [int(i) for i in (population_tested - np.array(progressive_TARs_data))], int(population_tested - net_cumulative_TAR_data), "None"
        else:
            return [int(i) for i in (population_tested - np.array(progressive_TARs_data))], int(population_tested - net_cumulative_TAR_data), int(population_tested - gross_cumulative_TAR_data)

    if data_type in {"data_type:dead", "dead", "data_type:mortality", "mortality", "data_type:threat", "threat"}:
        progressive_TARs, net_cumulative_TAR, gross_cumulative_TAR = calculate_cumulative_ARs_data()
    elif data_type in {"data_type:alive", "alive", "data_type:survival", "survival", "data_type:anti-threat", "anti-threat"}:
        progressive_TARs = progressive_TARs_data
        net_cumulative_TAR = "None" if not isinstance(net_cumulative_TAR_data, (int, float)) else net_cumulative_TAR_data
        gross_cumulative_TAR = "None" if not isinstance(gross_cumulative_TAR_data, (int, float)) else gross_cumulative_TAR_data
    else:
        raise ValueError ('Invalid data type command. Use one of: "data_type:dead" or "dead", "data_type:mortality" or "mortality", "data_type:alive" or "alive", "data_type:survival" or "survival", "data_type:threat" or "threat", "data_type:anti-threat" or "anti-threat" ')
    
    # Adaptive customization and optimization of parameters based on the exposuremetrics methodology
    centering = "centering:never" # The data has already been centered in the process above. No need for it through statistical mirroring function.
    pairing = "pairing:H_H"
    mirror_principal_value = min(progressive_TARs)
    ordering = "ordering:descend"
    
    # Function for estimating kc and its alternatives using p-sprox estimate
    def get_kcx(pprox_estimate, n_size):
        kc_sprox = kc_alt2(pprox_estimate, n_size)
        kcalt1_sprox = kc_alt1(pprox_estimate, n_size)
        kcalt2_sprox = kc_alt2(pprox_estimate, n_size)
        kcalt_sprox = kc_alt1(pprox_estimate, n_size)
        return [kc_sprox, kcalt1_sprox, kcalt2_sprox, kcalt_sprox]
        
    # Exposuremetrics analysis through statistical mirroring model calculations
    residual_estimates = stat_mirroring([
        progressive_TARs, 
        mirror_principal_value, 
        centering, ordering, 
        pairing, 
        "print:all_in_list"
    ])

    if method in {"method:residual", "residual"}:
        results = residual_estimates
    elif method in {"method:net", "net"}:
        if not isinstance(net_cumulative_TAR, (int, float)):
            results = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
        else:
            # Exposuremetrics analysis through statistical mirroring model calculations
            mirror_principal_value = net_cumulative_TAR
            results = stat_mirroring([
                progressive_TARs, 
                mirror_principal_value, 
                centering, 
                ordering, 
                pairing, 
                "print:all_in_list"
            ])
    
    elif method in {"method:gross", "gross"}:
        if not isinstance(gross_cumulative_TAR, (int, float)):
            results = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
        else:
            # Exposuremetrics analysis through statistical mirroring model calculations
            mirror_principal_value = gross_cumulative_TAR
            results = stat_mirroring([
                progressive_TARs, 
                mirror_principal_value, 
                centering, 
                ordering, 
                pairing, 
                "print:all_in_list"
            ])

    elif method in {"method:super residual", "super residual"}:
        """ 
        If superesidual = 0, it is called super nulliresidual
        If superesidual < 0, it is called super hyporesidual
        If superesidual > 0, it is called super hyperesidual
        """
        if not isinstance(net_cumulative_TAR, (int, float)):
            results = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
        else:
            # Exposuremetrics analysis through statistical mirroring model calculations
            mirror_principal_value = net_cumulative_TAR
            net_estimates = stat_mirroring([progressive_TARs,
                                             mirror_principal_value, 
                                             centering, ordering, 
                                             pairing, 
                                             "print:all_in_list"])
            super_residual_resistance =  residual_estimates[1] - net_estimates[1]
            super_residual_susceptibility =   residual_estimates[2] - net_estimates[2]
            kcs_values = get_kcx(super_residual_resistance, len(progressive_TARs))
            results = [kcs_values[0], super_residual_resistance, super_residual_susceptibility, kcs_values[1], kcs_values[2], kcs_values[3]]

    elif method in {"method:super net", "super net"}:
        """ 
        If supernet = 0, it is called super nullinet
        If supernet < 0, it is called super hyponet
        If supernet > 0, it is called super hypernet
        """
        if not isinstance(net_cumulative_TAR, (int, float)) or not isinstance(gross_cumulative_TAR, (int, float)):
            results = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
        else:
            # Exposuremetrics analysis through statistical mirroring model calculations
            mirror_principal_value_1 = net_cumulative_TAR
            mirror_principal_value_2 = gross_cumulative_TAR
            net_estimates = stat_mirroring([progressive_TARs, 
                                            mirror_principal_value_1, 
                                            centering, 
                                            ordering, 
                                            pairing, 
                                            "print:all_in_list"])
            gross_estimates = stat_mirroring([progressive_TARs, 
                                              mirror_principal_value_2, 
                                              centering, 
                                              ordering, 
                                              pairing, 
                                              "print:all_in_list"])
            super_net_resistance = net_estimates[1] - gross_estimates[1]
            super_net_susceptibility = net_estimates[2] - gross_estimates[2]
            kcs_values = get_kcx(super_net_resistance, len(progressive_TARs))
            results = [kcs_values[0], super_net_resistance, super_net_susceptibility, kcs_values[1], kcs_values[2], kcs_values[3]]
    
    elif method in {"method:super resnet", "super resnet"}:
        """ 
        If superesnet = 0, it is called super nullinet
        If superesnet < 0, it is called super hyponet
        If superesnet > 0, it is called super hypernet
        """
        if not isinstance(gross_cumulative_TAR, (int, float)):
            results = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
        else:
            # Exposuremetrics analysis through statistical mirroring model calculations
            mirror_principal_value = gross_cumulative_TAR
            gross_estimates = stat_mirroring([progressive_TARs, 
                                              mirror_principal_value, 
                                              centering, 
                                              ordering, 
                                              pairing, 
                                              "print:all_in_list"])
            super_resnet_resistance = residual_estimates[1] - gross_estimates[1]
            super_resnet_susceptibility = residual_estimates[2] - gross_estimates[2]
            kcs_values = get_kcx(super_resnet_resistance, len(progressive_TARs))
            results = [kcs_values[0], super_resnet_resistance, super_resnet_susceptibility, kcs_values[1], kcs_values[2], kcs_values[3]]
    
    else:
        raise ValueError ('Invalid method command. Use one of: "method:residual" or "residual", "method:net" or "net", "method:gross" or "gross", "method:super residual" or "super residual", "method:super net" or "super net", "method:super resnet" or "super resnet" ')
    
    # Printing the exposuremetrics estimates based on the provided print input command
    if print_result in {"print:kc-resistance", "kc-resistance"}:
        return results[0]
    elif print_result in {"print:p-resistance", "p-resistance"}:
        return results[1]
    elif print_result in {"print:p-susceptibility", "p-susceptibility"}:
        return results[2]
    elif print_result in {"print:kcalt1", "kcalt1"}:
        return results[3]
    elif print_result in {"print:kcalt2", "kcalt2"}:
        return results[4]
    elif print_result in {"print:kcalt", "kcalt"}:
        return results[5]
    elif print_result in {"print:all_in_list", "all_in_list"}:
        return [
                results[0],
                results[1],
                results[2],
                results[3],
                results[4],
                results[5]
                ]
    elif print_result in {"print:all_in_dict", "all_in_dict"}:
        return {
                "kc-resistance": results[0],
                "p-resistance": results[1],
                "p-susceptibility": results[2],
                "kcalt1": results[3],
                "kcalt2": results[4],
                "kcalt": results[5]
                }
    else:
        raise ValueError('Invalid print_result format. Use one of: "print:kc-resistance" or "kc-resistance", "print:p-resistance" or "p-resistance", "print:p-susceptibility" or "p-susceptibility",  "print:kcalt1", or "kcalt1", "print:kcalt2", or "kcalt2", "print:kcalt", "kcalt", "print:all_in_list" or all_in_list", or "print:all_in_dict", OR "all_in_dict" ')
        

def doc_qualitative_exposuremetrics():
    print("""
    Qualitative exposuremetrics is a measure of the biological proximity or deviation of an organism from the observed
    progressive threat or anti-threat responses to the expected cumulative threat or anti-threat responses (i.e., the residual,
    net, or gross expectation) as a result of exposure to a harmful agent(s). It estimates the organismal threat or
    anti-threat response dynamics of resistance and susceptibility within a population over successful events and generations.

    The organismal resistance is defined as the isoreflectivity (isoreflective pairing) of observed anti-threat
    responses to the expected cumulative anti-threat responses (i.e., the residual, net, or gross expectation).
    While organismal susceptibility is the deviation from attaining a complete and total resistance status.

    The process of exposuremetrics comprises four distinct phases:
            a)	Preprocessing (conceptualization, parameterization, adaptive customization and optimization) phase: This 
            phase forms the core of the methodology, defining key concepts and expectations derived from observed variables 
            to guide the design of the statistical mirror. It also involves customizing and optimizing parameters to ensure 
            the statistical mirroring process is well-suited to the specific analytical task.
            b)	Statistical Mirroring Analysis Phase **[Ref_2]**: This involves applying a suitable statistical mirroring type based on the 
            phase 1 adaption of the established adaptive customization and optimization of statistical mirroring parameters. 
            c)	Kabirian-based Optinalysis Model Calculation Phase **[Ref_3]**: This phase is focused on computing estimates 
            (such as the Kabirian coefficient of proximity, the probability of proximity, and the deviation) based on 
            Kabirian-based isomorphic optinalysis models. 
            d)  Advanced Exposuremetrics Calculations Phase **[Ref_1]**: These advanced metrics are the simple arithmetic differences 
            between qualitative exposuremetrics estimates.
    
    Args:
        input_list (list): A list containing the following 7 elements:
            - progressive threat or anti-threat responses (list): A list of responses at different exposure levels. E.g., mortality scores, 
            knockdown counts over periods during exposure.
            - net cumulative threat or anti-threat response (int, str): Observed cumulative threat or anti-threat response at a 
            specific period after exposure. 
            - gross cumulative threat or anti-threat response (int, str or "None"): Observed cumulative threat or anti-threat response from 
            a reference threshold (e.g., response due to synergist, or elicitor) at a specific period after exposure.
                * Note: These inputs (net and gross cumulative threat or anti-threat responses) are not neceaasary if the organisms were not 
                subjected to post-exposure treatment or others, you can write any non-numerical input (e.g., "Nil", "None", "Not recorded", e.t.c). 
                * However, you would not be able to calculate net or gross resistance and susceptibility estimates. 
            - population tested (int): The number of organisms tested or exposed.
            - data type (str): The number of organisms tested or exposed. Options can include one of:
                * "data_type:threat" or "threat", "data_type:mortality" or "mortality"           : For threat responses frequency.
                * "data_type:anti-threat" or "anti-threat", "data_type:survival" or "survival"   : For anti-threat responses frequency.
            - estimation method (str): The specific type of exposuremetrics analysis to compute. Options can include:
                * "method:residual" or "residual"   : Estimates residual resistance and susceptibility.
                * "method:net" or "net"             : Estimates net resistance and susceptibility.
                * "method:gross" or "gross"         : Estimates gross resistance and susceptibility.
                * "method:super residual" or "super residual"   : Estimates super residual resistance and susceptibility.
                * "method:super net" or "super net"             : Estimates super net resistance and susceptibility.
                * "method:super resnet" or "super resnet"       : Estimates super resnet resistance and susceptibility.
            - print_result (str): Specifies which type of result(s) to print or return. Options can include:
                * "print:kc-resistance" or "kc-resistance"           : Prints Kabirian coefficient of resistance.
                * "print:p-resistance" or "p-resistance"             : Prints probability of resistance.
                * "print:p-susceptibility" or "p-susceptibility"     : Prints probability of susceptibility.
                * "print:kcalt1" or "kcalt1" : Prints A-alternative Kabirian coefficient.
                * "print:kcalt2" or "kcalt2" : Prints D-alternative Kabirian coefficient.
                * "print:kcalt" or "kcalt"   : Prints the inverse alternative Kabirian coefficient.
                * "print:all_in_list" or "all_in_list"  : Prints all computed estimates in a list.
                * "print:all_in_dict" or "all_in_dict"  : Prints all computed estimates in a dictionary.

    Returns:
        float, list, dict, or str - Depending on the value of `print_result`, the function returns either a list or dictionary 
                       containing all the estimates or the requested specific estimate. If not suitable data, some estimates may return a string 'NaN'.

    Raises:
        ValueError: If the input data is not properly formatted or does not match the expected structure.

    Example:
        >>> import kbomodels as kbo
        
        # Parameters and input data
        >>> progressive_threat_responses = [0, 2, 7, 10, 12]   # Mortality counts/frequency in five (5) interval periods of repeating observations.  
        >>> net_cumulative_threat_response = 19               # If the value is not obtained, write any non-numerical input e.g: "None", "No record", e.t.c.
        >>> gross_cumulative_threat_response = 22             # If the value is not obtained, write any non-numerical input e.g: "None", "No record", e.t.c.
        >>> population_tested = 25
        >>> data_type = "threat"       # Because the recorded response data is the threat, therefore it will be checked converted in the computation process. 
        >>> estimation_method_1 = "residual"
        >>> estimation_method_2 = "net"
        >>> estimation_method_3 = "gross"
        >>> estimation_method_4 = "super residual"
        >>> print_outcomes = "print:all_in_dict"
        
        # Calculating the estimates
        >>> print(f" Residual estimates = {kbo.qualitative_exposuremetrics([progressive_threat_responses, net_cumulative_threat_response, gross_cumulative_threat_response, population_tested, data_type, estimation_method_1, print_outcomes])} ")
        >>> print(f" Net estimates = {kbo.qualitative_exposuremetrics([progressive_threat_responses, net_cumulative_threat_response, gross_cumulative_threat_response, population_tested, data_type, estimation_method_2, print_outcomes])} ")
        >>> print(f" Gross estimates = {kbo.qualitative_exposuremetrics([progressive_threat_responses, net_cumulative_threat_response, gross_cumulative_threat_response, population_tested, data_type, estimation_method_3, print_outcomes])} ")
        >>> print(f" Super residual estimates = {kbo.qualitative_exposuremetrics([progressive_threat_responses, net_cumulative_threat_response, gross_cumulative_threat_response, population_tested, data_type, estimation_method_4, print_outcomes])} ")
        
        # Outcomes
        Residual estimates = {'kc-resistance': 1.1425149700598805, 'p-resistance': 0.7396061269146605, 'p-susceptibility': 0.26039387308533946, 'kcalt1': 0.8890959925442683, 'kcalt2': 1.1425149700598807, 'kcalt': 0.8890959925442683} 
        
        Net estimates = {'kc-resistance': 1.4307692307692308, 'p-resistance': 0.46919431279620843, 'p-susceptibility': 0.5308056872037916, 'kcalt1': 0.7685950413223139, 'kcalt2': 1.4307692307692308, 'kcalt': 0.7685950413223139} 
        
        Gross estimates = {'kc-resistance': 1.6987012987012986, 'p-resistance': 0.33906633906633915, 'p-susceptibility': 0.6609336609336609, 'kcalt1': 0.7085590465872156, 'kcalt2': 1.6987012987012984, 'kcalt': 0.7085590465872156} 
        
        Super residual estimates = {'kc-resistance': 2.7888238618404055, 'p-resistance': 0.13012797372986928, 'p-susceptibility': -0.13012797372986928, 'kcalt1': 0.6092264040794205, 'kcalt2': 2.7888238618404055, 'kcalt': 0.6092264040794205} 

    **Process Overview:**
        1. Input Data Extraction and Formatting:
            - The function extracts the inputs: progressive threat or anti-threat responses, net cumulative threat or 
            anti-threat response, gross cumulative threat or anti-threat response, population tested, data type, method, 
            and the desired output format (print_result) from the provided `input_list`.

        2. Statistical Mirroring:
            - The function applies Kabirian-based isomorphic optinalysis, and statistical mirroring methodology, a method that preprocessed,
            orders, and pairs input numerical data for analysis. The specific mirroring setup in this function uses:
                * "centering:never" (no centering of the data),
                * "ordering:ascend" (data is ordered in descending order),
                * "pairing:H_H" (the lowest ends of the isoreflective pair of points are maximally distant).
        
        3. Advance Exposuremetrics Analysis:
            - These advanced metrics are the simple arithmetic differences between the qualitative exposuremetrics estimates. 
        
        4. Customized Output:
            - Based on the `print_result` parameter, the function customizes the returned results.
            The user can request print only a specific result or all computed statistics.

    **Notes:**
            - This function relies on the `Kabirian-based isomorphic optinalysis`, and `statistical mirroring` function, which implements the core 
            qualitative exposuremetrics function for exposuremetrics data analysis of qualitative variable. 
            - Ensure the `statistical mirroring` and
            `D-alternative Kabirian coefficient (kcalt2)` functions are properly imported and defined in the same context.

    **References:**
        *Cite these references to acknowledge the methodologies:* 
        **[Ref_1]** Abdullahi, K. B.; Suleiman, M.; Wagini, N. H.; Sani, I. (2025). qualitative exposuremetrics: A comprehensive and sensitive estimation
        framework for analyzing organismal resistance and susceptibility dynamics using qualitative variables. 
        [You can follow updates for the published citation details].

        **[Ref_2]** Abdullahi, K. B. (2024). Statistical mirroring: A robust method for statistical dispersion estimation. 
        MethodsX, 12, 102682. https://doi.org/10.1016/j.mex.2024.102682 
        
        **[Ref_3]** Abdullahi, K. B. (2023). Kabirian-based optinalysis: A conceptually grounded framework for symmetry/asymmetry, 
        similarity/dissimilarity and identity/unidentity estimations in mathematical structures and biological sequences. 
        MethodsX, 11, 102400. https://doi.org/10.1016/j.mex.2023.102400 

        *Cite these references to acknowledge the Python codes implementation of the methodologies:*
        **[Ref_1]** Abdullahi, K. B. (2025). Python code for qualitative exposuremetrics analysis.
        Mendeley Data, V1. doi: 10.17632/xk38tj5vbw.1 (https://data.mendeley.com/datasets/xk38tj5vbw/1) 

        **[Ref_2]** Abdullahi, K. B. (2024). A Python code for statistical mirroring. Mendeley Data, V4. 
        doi: 10.17632/ppfvc65m2v.4 (https://data.mendeley.com/datasets/ppfvc65m2v/4)

        **[Ref_3]** Abdullahi, K. B. (2024). Python codes for Kabirian-based automorphic and isomorphic optinalysis. 
        Mendeley Data, V3. doi: 10.17632/gnrcj8s7fp.3 (https://data.mendeley.com/datasets/gnrcj8s7fp/3) 
    """)
