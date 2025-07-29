_B=True
_A=None
import logging,csv,re
from scilens.readers.reader_interface import ReaderInterface
from scilens.readers.cols_dataset import ColsDataset,ColsCurves,cols_dataset_get_curves_col_x,compare as cols_compare
from scilens.readers.mat_dataset import MatDataset,from_iterator as mat_from_iterator,compare as mat_compare,get_data
from scilens.config.models.reader_format_csv import ReaderCsvConfig,ReaderCsvMatrixConfig
from scilens.config.models.reader_format_cols import ReaderCurveParserNameConfig
from scilens.components.compare_models import CompareGroup
from scilens.components.compare_floats import CompareFloats
def is_num(x):
	try:return float(x)
	except ValueError:return
def csv_row_detect_header(first_row):
	A=first_row
	if all(not A.isdigit()for A in A):return _B,A
	else:return False,[f"Column {A}"for(A,B)in enumerate(A)]
def csv_row_detect_cols_num(row):return[A for(A,B)in enumerate(row)if is_num(B)!=_A]
def csv_detect(path,delimiter,quotechar,encoding):
	with open(path,'r',encoding=encoding)as B:A=csv.reader(B,delimiter=delimiter,quotechar=quotechar);C=next(A);D,E=csv_row_detect_header(C);F=next(A);G=csv_row_detect_cols_num(F);return D,E,G
class ReaderCsv(ReaderInterface):
	configuration_type_code='csv';category='datalines';extensions=['CSV']
	def read(A,reader_options):
		B=reader_options;A.reader_options=B;K=B.ignore_lines_patterns;A.raw_lines_number=_A;A.curves=_A;A.report_matrices=_A;D,G,R=csv_detect(A.origin.path,A.reader_options.delimiter,A.reader_options.quotechar,encoding=A.encoding);A.has_header=D;A.cols=G;A.numeric_col_indexes=R;L=B.lines.start if B.lines and B.lines.start else _A;M=B.lines.end if B.lines and B.lines.end else _A
		with open(A.origin.path,'r',encoding=A.encoding)as S:
			N=S.readlines();H=csv.reader(N,delimiter=A.reader_options.delimiter,quotechar=A.reader_options.quotechar)
			if B.is_matrix:
				F=B.matrix or ReaderCsvMatrixConfig();I=mat_from_iterator(x_name=F.x_name,y_name=F.y_name,reader=H,has_header=D,x_value_line=F.x_value_line,has_y=F.has_y)
				if F.export_report:A.report_matrices=get_data([I],['csv'])
				A.mat_dataset=I;A.raw_lines_number=I.nb_lines+(1 if D else 0)
			else:
				if B.ignore_columns:
					if not D:raise Exception('Ignore columns is not supported without header.')
					A.numeric_col_indexes=[C for C in A.numeric_col_indexes if A.cols[C]not in B.ignore_columns]
				O=len(G);C=ColsDataset(cols_count=O,names=G,numeric_col_indexes=A.numeric_col_indexes,data=[[]for A in range(O)]);E=0
				if L:
					for X in range(L-1):
						try:next(H);E+=1
						except StopIteration:break
				try:
					while _B:
						T=next(H);E+=1
						if M and E>M:break
						if D and E==1:continue
						if K:
							U=N[E-1].rstrip('\n');P=False
							for V in K:
								if bool(re.match(V,U)):P=_B;break
							if P:continue
						for(Q,J)in enumerate(T):
							if Q in C.numeric_col_indexes:J=float(J)
							C.data[Q].append(J)
						C.origin_line_nb.append(E)
				except StopIteration:pass
				C.rows_count=len(C.origin_line_nb);A.cols_dataset=C;A.raw_lines_number=C.rows_count+(1 if D else 0)
				if B.curve_parser:
					if B.curve_parser.name==ReaderCurveParserNameConfig.COL_X:
						A.curves,W=cols_dataset_get_curves_col_x(C,B.curve_parser.parameters.x)
						if A.curves:A.cols_curve=ColsCurves(type=ReaderCurveParserNameConfig.COL_X,info=W,curves=A.curves)
					elif B.curve_parser.name==ReaderCurveParserNameConfig.COLS_COUPLE:raise NotImplementedError('cols_couple not implemented')
					else:raise Exception('Curve parser not supported.')
	def compare(A,compare_floats,param_reader,param_is_ref=_B):
		H='node';D=param_is_ref;C=param_reader;B=compare_floats;I=A.reader_options
		if I.is_matrix:E=A.mat_dataset if D else C.mat_dataset;F=A.mat_dataset if not D else C.mat_dataset;J,G=B.compare_errors.add_group(H,'csv matrix');mat_compare(G,B,E,F)
		else:E=A.cols_dataset if D else C.cols_dataset;F=A.cols_dataset if not D else C.cols_dataset;K=A.cols_curve if hasattr(A,'cols_curve')else _A;J,G=B.compare_errors.add_group(H,'csv cols');cols_compare(G,B,E,F,K)
	def class_info(A):return{'cols':A.cols,'raw_lines_number':A.raw_lines_number,'curves':A.curves,'matrices':A.report_matrices}