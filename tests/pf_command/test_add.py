import unittest

from pf_manager.pf_command.add import AddCommand


class TestPfm(unittest.TestCase):
    def test_generate_target_with_options(self):
        add_command = AddCommand("image-processing",
                                 None, "L",
                                 "localhost", "8888", "8888",
                                 "my.aws.com", None, None, None)
        result = add_command.generate_target()
        self.assertEqual(result["type"], "L")
        self.assertEqual(result["name"], "image-processing")
        self.assertEqual(result["local_port"], "8888")

    def test_generate_target_with_argument(self):
        add_command = AddCommand("image-processing",
                                 "8888:localhost:8888 root@workbench.aws.com",
                                 None, None, None, None, None, None, None, None)
        result = add_command.generate_target()
        self.assertEqual(result["type"], "L")
        self.assertEqual(result["name"], "image-processing")
        self.assertEqual(result["local_port"], "8888")
        self.assertEqual(result["ssh_server"], "workbench.aws.com")
        self.assertEqual(result["login_user"], "root")

    def test_raise_exception_with_inadiquate_parameters(self):
        add_command = AddCommand("image-processing", None, "L",
                                 "localhost", None, "8888",
                                 None, None, None, None)
        self.assertRaises(RuntimeError, lambda: add_command.generate_consistent_target({}))

    def test_add_same_local_port(self):
        targets = {'food-nonfood': {
                'name': 'text-classification',
                'local_port': '8888', 'login_user': None,
                'remote_port': '9999', 'server_port': None,
                'type': 'L', 'remote_host': 'localhost',
                'ssh_server': 'my-ml-instance.ml.aws.com'
            }
        }
        add_command = AddCommand("image-processing", None, "L", "localhost",
                                 "8888", "8888", "my.aws.com", None, None,
                                 None)
        self.assertEqual("8888", add_command.generate_consistent_target(targets)["local_port"])

    def test_add_target_without_local_port(self):
        targets = {'food-nonfood': {
                'name': 'text-classification',
                'local_port': '6000', 'login_user': None,
                'remote_port': '9999', 'server_port': None,
                'type': 'L', 'remote_host': 'localhost',
                'ssh_server': 'my-ml-instance.ml.aws.com'
            }
        }
        add_command = AddCommand("image-processing",
                                 None, "L", "localhost", "8888",
                                 None, "my.aws.com", None, None, None)
        self.assertEqual("49152", add_command.generate_consistent_target(targets)["local_port"])

    def test_add_target_without_remote_port(self):
        targets = {'food-nonfood': {
                'name': 'text-classification',
                'local_port': '8888', 'login_user': None,
                'remote_port': '6000', 'server_port': None,
                'type': 'L', 'remote_host': 'localhost',
                'ssh_server': 'my-ml-instance.ml.aws.com'
            }
        }
        add_command = AddCommand("image-processing", None, "L",
                                 "localhost", None, None,
                                 "my-ml-instance.ml.aws.com", None, None, None)
        self.assertEqual("49152", add_command.generate_consistent_target(targets)["remote_port"])

    def test_add_same_remote_port_in_different_host(self):
        targets = {'food-nonfood': {
                'name': 'text-classification',
                'local_port': '8888',
                'login_user': None, 'remote_port': '9999',
                'server_port': None, 'type': 'L', 'remote_host': 'my-ml-instance-2.ml.aws.com',
                'ssh_server': 'my-ml-instance.ml.aws.com'
            }
        }
        add_command = AddCommand("image-processing", None,
                                 "L", "my-ml-instance.ml-1.aws.com", "9999", "7777",
                                 "ssh-server-instance.ml.aws.com", None, None, None)
        self.assertEqual("9999", add_command.generate_consistent_target(targets)["remote_port"])

    def test_fail_to_add_same_remote_port_in_same_host(self):
        targets = {'food-nonfood': {
                'name': 'text-classification',
                'local_port': '8888', 'login_user': None,
                'remote_port': '9999', 'server_port': None,
                'type': 'L', 'remote_host': 'my-ml-instance.ml.aws.com',
                'ssh_server': 'my-ml-instance.ml.aws.com'
            }
        }
        add_command = AddCommand("image-processing", None, "L",
                                 "my-ml-instance.ml.aws.com", "9999", "7777",
                                 "ssh-server-instance.ml.aws.com", None, None, None)
        self.assertEqual("9999", add_command.generate_consistent_target(targets)["remote_port"])

    def test_fail_to_add_same_remote_port_in_same_host2(self):
        targets = {'food-nonfood': {
                'name': 'text-classification',
                'local_port': '8888', 'login_user': None, 'remote_port': '9999', 'server_port': None,
                'type': 'L', 'remote_host': 'localhost', 'ssh_server': 'my-ml-instance.ml.aws.com'
            }
        }
        add_command = AddCommand("image-processing", None, 'L', 'localhost', '9999', '7777',
                                 'my-ml-instance.ml.aws.com', None, None,
                                 None)
        self.assertEqual("9999", add_command.generate_consistent_target(targets)["remote_port"])
