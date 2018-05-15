
import os

def test_ReplaceStrInFile():
    fileName = "D:\\Program_files\\Perforce\\pitaya_1667_new\\Verification_scripts\\Elite3000\WBU\Dual_Source\\Blending\\WBU_R8G8_UNORM_Dual_Src_BLEND_SRC1_ALPHA.s3s"
    dirName = os.path.split(fileName)[0]
    relativeFileName = os.path.split(fileName)[1]
    print dirName
    print relativeFileName