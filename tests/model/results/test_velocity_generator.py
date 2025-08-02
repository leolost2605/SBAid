import unittest
from sbaid.common.diagram_type import DiagramType
from sbaid.model.results.velocity_generator import VelocityGenerator

class VelocityGeneratorTest(unittest.TestCase):

    generator = VelocityGenerator()

    def test_get_diagram_type(self):
        """Tests if the get diagram type method returns a diagram
        type instance with the desired values. """
        diagram_type = self.generator.get_diagram_type()
        self.assertIsInstance(diagram_type, DiagramType)
        self.assertEqual(diagram_type.name, "Velocity-Diagram")
        self.assertEqual(diagram_type.diagram_type_id, "Velocity-Diagram")
