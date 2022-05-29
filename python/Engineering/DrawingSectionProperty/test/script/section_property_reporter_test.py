import unittest
import subprocess
import os
from shutil import copyfile
from src.util.constants import Constants


class SectionPropertyReporterTest(unittest.TestCase):

    def test_script_01(self):
        """
        Long report
        1 File
        1 Profile
        No Material
        """
        file_input = "testdata001.dxf"
        output_file = os.path.splitext(file_input)[0] + ".pdf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)

        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)
        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file)))

    def test_script_02(self):
        """
        Short report
        1 File
        1 Profile
        No Material
        """
        file_input = "testdata001.dxf"
        output_file = os.path.splitext(file_input)[0] + ".pdf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)

        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -hole"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file)))

    def test_script_03(self):
        """
        Long report
        1 File
        1 Profile
        1 Material
        """
        file_input = "testdata001.dxf"
        output_file = os.path.splitext(file_input)[0] + ".pdf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)

        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole -m aluminum_ams_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file)))

    def test_script_04(self):
        """
        Short report
        1 File
        1 Profile
        1 Material
        """
        file_input = "testdata001.dxf"
        output_file = os.path.splitext(file_input)[0] + ".pdf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)

        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -hole -m aluminum_ams_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file)))

    def test_script_05(self):
        """
        Long report
        1 File
        1 Profile
        2 Material
        """
        file_input = "testdata001.dxf"
        output_file = os.path.splitext(file_input)[0] + ".pdf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)

        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole -m aluminum_ams_nmms carbon_steel_ams_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file)))

    def test_script_06(self):
        """
        Short report
        1 File
        1 Profile
        2 Material
        """
        file_input = "testdata001.dxf"
        output_file = os.path.splitext(file_input)[0] + ".pdf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)

        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -hole -m aluminum_ams_nmms carbon_steel_ams_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file)))

    def test_script_07(self):
        """
        Long report
        1 File
        1 Profile
        2 Material
        Weighted
        """
        file_input = "testdata001.dxf"
        output_file = os.path.splitext(file_input)[0] + ".pdf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)

        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -weighted -hole -m aluminum_ams_nmms carbon_steel_ams_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file)))

    def test_script_08(self):
        """
        Short report
        1 File
        1 Profile
        2 Material
        Weighted
        """
        file_input = "testdata001.dxf"
        output_file = os.path.splitext(file_input)[0] + ".pdf"
        testdata_file_path = os.path.join(Constants.TEST_DIR, "testdata", file_input)

        src = testdata_file_path
        dest = os.path.join(Constants.INPUT_DIR, file_input)
        copyfile(src, dest)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -weighted -hole -m aluminum_ams_nmms carbon_steel_ams_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file)))

    def test_script_09(self):
        """
        Long report
        2 File
        File1 = 1 Profile
        File2 = 1 Profile
        No Material
        """
        file_input1 = "testdata001.dxf"
        output_file1 = os.path.splitext(file_input1)[0] + ".pdf"
        testdata_file_path1 = os.path.join(Constants.TEST_DIR, "testdata", file_input1)

        src = testdata_file_path1
        dest1 = os.path.join(Constants.INPUT_DIR, file_input1)
        copyfile(src, dest1)

        file_input2 = "testdata002.dxf"
        output_file2 = os.path.splitext(file_input2)[0] + ".pdf"
        testdata_file_path2 = os.path.join(Constants.TEST_DIR, "testdata", file_input2)

        src = testdata_file_path2
        dest2 = os.path.join(Constants.INPUT_DIR, file_input2)
        copyfile(src, dest2)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest1)
        os.remove(dest2)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file1)))
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file2)))

    def test_script_10(self):
        """
        Short report
        2 File
        File1 = 1 Profile
        File2 = 1 Profile
        No Material
        """
        file_input1 = "testdata001.dxf"
        output_file1 = os.path.splitext(file_input1)[0] + ".pdf"
        testdata_file_path1 = os.path.join(Constants.TEST_DIR, "testdata", file_input1)

        src = testdata_file_path1
        dest1 = os.path.join(Constants.INPUT_DIR, file_input1)
        copyfile(src, dest1)

        file_input2 = "testdata002.dxf"
        output_file2 = os.path.splitext(file_input2)[0] + ".pdf"
        testdata_file_path2 = os.path.join(Constants.TEST_DIR, "testdata", file_input2)

        src = testdata_file_path2
        dest2 = os.path.join(Constants.INPUT_DIR, file_input2)
        copyfile(src, dest2)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -hole"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest1)
        os.remove(dest2)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file1)))
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file2)))

    def test_script_11(self):
        """
        Long report
        2 File
        File1 = 1 Profile
        File2 = 1 Profile
        2 Material
        """
        file_input1 = "testdata001.dxf"
        output_file1 = os.path.splitext(file_input1)[0] + ".pdf"
        testdata_file_path1 = os.path.join(Constants.TEST_DIR, "testdata", file_input1)

        src = testdata_file_path1
        dest1 = os.path.join(Constants.INPUT_DIR, file_input1)
        copyfile(src, dest1)

        file_input2 = "testdata002.dxf"
        output_file2 = os.path.splitext(file_input2)[0] + ".pdf"
        testdata_file_path2 = os.path.join(Constants.TEST_DIR, "testdata", file_input2)

        src = testdata_file_path2
        dest2 = os.path.join(Constants.INPUT_DIR, file_input2)
        copyfile(src, dest2)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole -m aluminum_ams_nmms carbon_steel_bs_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest1)
        os.remove(dest2)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file1)))
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file2)))

    def test_script_12(self):
        """
        Long report
        2 File
        File1 = 1 Profile
        File2 = 1 Profile
        1 Material
        """
        file_input1 = "testdata001.dxf"
        output_file1 = os.path.splitext(file_input1)[0] + ".pdf"
        testdata_file_path1 = os.path.join(Constants.TEST_DIR, "testdata", file_input1)

        src = testdata_file_path1
        dest1 = os.path.join(Constants.INPUT_DIR, file_input1)
        copyfile(src, dest1)

        file_input2 = "testdata002.dxf"
        output_file2 = os.path.splitext(file_input2)[0] + ".pdf"
        testdata_file_path2 = os.path.join(Constants.TEST_DIR, "testdata", file_input2)

        src = testdata_file_path2
        dest2 = os.path.join(Constants.INPUT_DIR, file_input2)
        copyfile(src, dest2)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole -m carbon_steel_bs_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest1)
        os.remove(dest2)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file1)))
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file2)))

    def test_script_13(self):
        """
        Long report
        2 File
        File1 = 1 Profile
        File2 = 1 Profile
        3 Material
        """
        file_input1 = "testdata001.dxf"
        output_file1 = os.path.splitext(file_input1)[0] + ".pdf"
        testdata_file_path1 = os.path.join(Constants.TEST_DIR, "testdata", file_input1)

        src = testdata_file_path1
        dest1 = os.path.join(Constants.INPUT_DIR, file_input1)
        copyfile(src, dest1)

        file_input2 = "testdata002.dxf"
        output_file2 = os.path.splitext(file_input2)[0] + ".pdf"
        testdata_file_path2 = os.path.join(Constants.TEST_DIR, "testdata", file_input2)

        src = testdata_file_path2
        dest2 = os.path.join(Constants.INPUT_DIR, file_input2)
        copyfile(src, dest2)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole -m carbon_steel_bs_nmms aluminum_ams_nmms stainless_steel_bs_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest1)
        os.remove(dest2)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file1)))
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file2)))

    def test_script_14(self):
        """
        Long report
        2 File
        File1 = 1 Profile
        File2 = 2 Profile
        3 Material
        """
        file_input1 = "testdata001.dxf"
        output_file1 = os.path.splitext(file_input1)[0] + ".pdf"
        testdata_file_path1 = os.path.join(Constants.TEST_DIR, "testdata", file_input1)

        src = testdata_file_path1
        dest1 = os.path.join(Constants.INPUT_DIR, file_input1)
        copyfile(src, dest1)

        file_input2 = "testdata009.dxf"
        output_file2 = os.path.splitext(file_input2)[0] + ".pdf"
        testdata_file_path2 = os.path.join(Constants.TEST_DIR, "testdata", file_input2)

        src = testdata_file_path2
        dest2 = os.path.join(Constants.INPUT_DIR, file_input2)
        copyfile(src, dest2)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole -m carbon_steel_bs_nmms aluminum_ams_nmms stainless_steel_bs_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest1)
        os.remove(dest2)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file1)))
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file2)))

    def test_script_15(self):
        """
        Long report
        2 File
        File1 = 1 Profile
        File2 = 2 Profile
        2 Material
        """
        file_input1 = "testdata001.dxf"
        output_file1 = os.path.splitext(file_input1)[0] + ".pdf"
        testdata_file_path1 = os.path.join(Constants.TEST_DIR, "testdata", file_input1)

        src = testdata_file_path1
        dest1 = os.path.join(Constants.INPUT_DIR, file_input1)
        copyfile(src, dest1)

        file_input2 = "testdata009.dxf"
        output_file2 = os.path.splitext(file_input2)[0] + ".pdf"
        testdata_file_path2 = os.path.join(Constants.TEST_DIR, "testdata", file_input2)

        src = testdata_file_path2
        dest2 = os.path.join(Constants.INPUT_DIR, file_input2)
        copyfile(src, dest2)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole -m carbon_steel_bs_nmms aluminum_ams_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest1)
        os.remove(dest2)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file1)))
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file2)))

    def test_script_16(self):
        """
        Long report
        2 File
        File1 = 1 Profile
        File2 = 2 Profile
        4 Material
        """
        file_input1 = "testdata001.dxf"
        output_file1 = os.path.splitext(file_input1)[0] + ".pdf"
        testdata_file_path1 = os.path.join(Constants.TEST_DIR, "testdata", file_input1)

        src = testdata_file_path1
        dest1 = os.path.join(Constants.INPUT_DIR, file_input1)
        copyfile(src, dest1)

        file_input2 = "testdata009.dxf"
        output_file2 = os.path.splitext(file_input2)[0] + ".pdf"
        testdata_file_path2 = os.path.join(Constants.TEST_DIR, "testdata", file_input2)

        src = testdata_file_path2
        dest2 = os.path.join(Constants.INPUT_DIR, file_input2)
        copyfile(src, dest2)

        main_fp = os.path.join(Constants.ROOT_DIR, 'main.py')
        command_str = f"python {main_fp} -long -hole -m aluminum_ams_nmms aluminum_bs_nmms carbon_steel_ams_nmms " + \
                      "carbon_steel_bs_nmms"
        command_args = command_str.split(" ")
        process = subprocess.Popen(command_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(output.decode("utf-8"))
        os.remove(dest1)
        os.remove(dest2)
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file1)))
        self.assertTrue(os.path.exists(os.path.join(Constants.OUTPUT_DIR, output_file2)))
