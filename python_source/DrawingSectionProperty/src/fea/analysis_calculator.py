class AnalysisCalculator:

    @classmethod
    def calculate_section_properties(cls, cross_section):
        cross_section.calculate_geometric_properties()
        cross_section.calculate_plastic_properties()
        cross_section.calculate_warping_properties()
        return cross_section
