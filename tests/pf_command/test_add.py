import unittest

from pf_manager.pf_command.add import AddCommand


class TestPfm(unittest.TestCase):
    def test_generate_target_with_options(self):
        add_command = AddCommand("image-processing", None, "L", "localhost", "8888", "8888", "my.aws.com", None, None,
                                 None)
        result = add_command.generate_target()
        self.assertEqual(result["type"], "L")
        self.assertEqual(result["name"], "image-processing")
        self.assertEqual(result["local_port"], "8888")

    def test_generate_target_with_argument(self):
        add_command = AddCommand("image-processing", "8888:localhost:8888 root@workbench.aws.com", None, None, None,
                                 None, None, None, None, None)
        result = add_command.generate_target()
        self.assertEqual(result["type"], "L")
        self.assertEqual(result["name"], "image-processing")
        self.assertEqual(result["local_port"], "8888")
        self.assertEqual(result["ssh_server"], "workbench.aws.com")
        self.assertEqual(result["login_user"], "root")

    def test_raise_exception_with_inadiquate_parameters(self):
        add_command = AddCommand("image-processing", None, "L", "localhost", None, "8888", "my.aws.com", None, None,
                                 None)
        self.assertRaises(RuntimeError, add_command.generate_target)
