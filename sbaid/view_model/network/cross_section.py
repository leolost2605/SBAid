from common.cross_section_type import CrossSectionType
from common.location import Location
from model.network import cross_section

from gi.repository import GObject


class CrossSection(GObject.GObject):
    """TODO"""
    id = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE |
                                          GObject.ParamFlags.WRITABLE |
                                          GObject.ParamFlags.CONSTRUCT_ONLY)
    name = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE |
                                            GObject.ParamFlags.WRITABLE |
                                            GObject.ParamFlags.CONSTRUCT)
    location = GObject.Property(type=Location, flags=GObject.ParamFlags.READABLE |
                                                     GObject.ParamFlags.WRITABLE |
                                                     GObject.ParamFlags.CONSTRUCT_ONLY)
    type = GObject.Property(type=CrossSectionType, default=CrossSectionType.COMBINED,
                            flags=GObject.ParamFlags.READABLE |
                                  GObject.ParamFlags.WRITABLE |
                                  GObject.ParamFlags.CONSTRUCT_ONLY)
    lanes = GObject.Property(type=int, flags=GObject.ParamFlags.READABLE |
                                             GObject.ParamFlags.WRITABLE |
                                             GObject.ParamFlags.CONSTRUCT_ONLY)
    hard_shoulder_available = GObject.Property(type=bool, default=False,
                                               flags=GObject.ParamFlags.READABLE |
                                                     GObject.ParamFlags.WRITABLE |
                                                     GObject.ParamFlags.CONSTRUCT_ONLY)
    hard_shoulder_active = GObject.Property(type=bool, default=False,
                                            flags=GObject.ParamFlags.READABLE |
                                                  GObject.ParamFlags.WRITABLE |
                                                  GObject.ParamFlags.CONSTRUCT)
    b_display_active = GObject.Property(type=bool, default=False,
                                        flags=GObject.ParamFlags.READABLE |
                                              GObject.ParamFlags.WRITABLE |
                                              GObject.ParamFlags.CONSTRUCT)

    def __init__(self, m_cross_section: cross_section.CrossSection):
        """TODO"""
        self._model_cross_section = cross_section
        m_id = m_cross_section.id  # TODO like this???
        m_name = m_cross_section.name
        m_position = m_cross_section.position
        m_type = m_cross_section.type
        m_lanes = m_cross_section.lanes
        m_hard_shoulder_available = m_cross_section.hard_shoulder_available
        m_hard_shoulder_active = m_cross_section.hard_shoulder_active
        m_b_display_active = m_cross_section.b_display_active
        super().__init__(id=m_id, name=m_name, position=m_position, type=m_type, lanes=m_lanes,
                         hard_shoulder_available=m_hard_shoulder_available,
                         hard_shoulder_active=m_hard_shoulder_active,
                         b_display_active=m_b_display_active)

