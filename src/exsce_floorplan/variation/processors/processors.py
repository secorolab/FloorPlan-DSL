from textx import TextXSemanticError, get_location

def discrete_distribution_obj_processor(discrete):

    p_sum = sum(discrete.probabilitities)
    if not p_sum == 1:
        raise TextXSemanticError('discrete distirbution must sum to 1', 
                                **get_location(discrete))