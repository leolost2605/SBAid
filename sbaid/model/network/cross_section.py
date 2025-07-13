class CrossSection:
    """TODO"""
    def __init__(self, simulator_cross_section: SimulatorCrossSection):
        self.cs_id: str
        self.cs_name: str
        self.position: Coordinate
        self.cs_type: Common.CrossSectionType
        self.lanes: int
        self.hard_shoulder_available: bool
        self.hard_shoulder_active: bool
        self.b_display_active: bool

    def load_from_db(self):
        """TODO"""
