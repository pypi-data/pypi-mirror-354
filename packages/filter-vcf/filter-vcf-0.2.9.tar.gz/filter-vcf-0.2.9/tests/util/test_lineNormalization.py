from unittest import TestCase
from unittest.mock import patch, Mock, call

from filter_vcf.util.lineNormalization import normalize_vcf_line, perform_line_normalization
from tests.utils import FileMock

line = "1	35910077	rs1293956811	A	G	.	.	RS=1293956811;RSPOS=35910077;dbSNPBuildID=151;SSR=0;SAO=0;VP=0x050000080005000002000100;GENEINFO=RCAN1:1827"
logger = Mock()


class TestNormalizeVCFLine(TestCase):
    @patch("filter_vcf.util.lineNormalization.filter_line", return_value=line)
    @patch("filter_vcf.util.lineNormalization.add_depth_to_line", return_value=line)
    @patch("filter_vcf.util.lineNormalization.filter_non_ref_from_line", return_value=line)
    @patch("filter_vcf.util.lineNormalization.keep_unique_line", return_value=line)
    def test_normalize_vcf_line(
        self,
        mock_keep_unique_line: Mock,
        mock_filter_non_ref_from_line: Mock,
        mock_add_depth_to_line: Mock,
        mock_filter_line: Mock,
    ):
        result = normalize_vcf_line(line, None, {"filters": "PASS", "depth": True, "unique": True})

        self.assertEqual(result, f"{line}\n")
        mock_filter_line.assert_called_once_with(line, "PASS")
        mock_add_depth_to_line.assert_called_once_with(line)
        mock_filter_non_ref_from_line.assert_called_once_with(line)
        mock_keep_unique_line.assert_called_once_with(line, None)

    @patch("filter_vcf.util.lineNormalization.filter_line", return_value=None)
    @patch("filter_vcf.util.lineNormalization.add_depth_to_line", return_value=None)
    @patch("filter_vcf.util.lineNormalization.filter_non_ref_from_line", return_value=None)
    @patch("filter_vcf.util.lineNormalization.keep_unique_line", return_value=None)
    def test_normalize_vcf_line_with_none(self, *_):
        result = normalize_vcf_line("", None, {"filters": "PASS", "depth": True, "unique": True})

        self.assertEqual(result, None)

    def test_normalize_caris_liquid_vcf_line(self):
        caris_liquid_line = "chr1	65529	.	C	T	.	base_qual;contamination;haplotype;weak_evidence	AS_FilterStatus=weak_evidence,base_qual,contamination;AS_SB_TABLE=0,0|0,0;DP=0;ECNT=2;GERMQ=93;MBQ=40,0;MFRL=0,0;MMQ=60,60;MPOS=50;POPAF=7.3;TLOD=7;TI=NM_001005484.1;GI=OR4F5;FC=Silent;DC=c.-3562C>T;LO=UPSTREAM	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0/1:0,0:0.5:0:0,0:0,0:0|1:65529_C_T:65529:0,0,0,0"
        result = normalize_vcf_line(
            caris_liquid_line, None, {"filters": "CarisLiquid", "depth": True, "unique": True}
        )


test_data = [
    "# header line",
    "variant line",
]


class TestPerformLineNormalization(TestCase):
    @patch("filter_vcf.util.lineNormalization.normalize_vcf_line", return_value="variant line")
    @patch("os.rename")
    @patch("gzip.open")
    def test_perform_line_normalization(
        self,
        mock_gzip_open: Mock,
        mock_rename: Mock,
        mock_normalize_vcf_line: Mock,
    ):
        mock_write = Mock()
        mock_gzip_open.return_value.__enter__.return_value = FileMock(test_data, mock_write)

        perform_line_normalization("in.vcf", "/tmp", {"filters": "PASS", "depth": True}, logger)

        mock_rename.assert_called_once_with("in.vcf", "/tmp/working.vcf.gz")
        mock_gzip_open.assert_any_call("/tmp/working.vcf.gz", "rt")
        mock_gzip_open.assert_any_call("in.vcf", "wt")
        mock_normalize_vcf_line.assert_called_once_with(
            "variant line", None, {"filters": "PASS", "depth": True}
        )
        mock_write.assert_has_calls([call("# header line"), call("variant line")])
