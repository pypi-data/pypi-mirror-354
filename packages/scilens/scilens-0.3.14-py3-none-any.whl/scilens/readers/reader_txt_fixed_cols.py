_A=None
import logging,re
from itertools import islice
from dataclasses import dataclass
from scilens.readers.transform import string_2_float
from scilens.readers.reader_interface import ReaderInterface
from scilens.readers.cols_dataset import ColsDataset,ColsCurves,cols_dataset_get_curves_col_x,compare
from scilens.config.models import ReaderTxtFixedColsConfig
from scilens.config.models.reader_format_cols import ReaderCurveParserNameConfig
from scilens.components.compare_floats import CompareFloats
@dataclass
class ParsedHeaders:raw:str;cleaned:str;data:list[str];ori_line_idx:int|_A=_A
class ReaderTxtFixedCols(ReaderInterface):
	configuration_type_code='txt_fixed_cols';category='datalines';extensions=[]
	def _ignore_line(A,line):
		if not line.strip():return True
		if A.reader_options.ignore_lines_patterns:
			for B in A.reader_options.ignore_lines_patterns:
				if bool(re.match(B,line)):return True
		return False
	def _get_parsed_headers(A,path):
		B=A.reader_options;C=_A
		with open(A.origin.path,'r',encoding=A.encoding)as G:
			D=-1
			if B.has_header_line is not _A:
				for E in G:
					D+=1
					if D+1==B.has_header_line:C=E;break
			else:
				for E in G:
					D+=1
					if not A._ignore_line(E):C=E;break
		if C:
			H=C.strip();F=H
			if B.has_header_ignore:
				for I in B.has_header_ignore:F=F.replace(I,'')
			return ParsedHeaders(raw=H,cleaned=F,data=F.split(),ori_line_idx=D)
	def _get_first_data_line(A,path):
		D=A.reader_options;B=D.has_header
		with open(A.origin.path,'r',encoding=A.encoding)as E:
			for C in E:
				if not A._ignore_line(C):
					if B:B=False;continue
					else:return C
	def _discover_col_idx_ralgin_spaces(G,line):
		A=line;A=A.rstrip();C=[];D=_A;B=0
		for(E,F)in enumerate(A):
			if D is not _A and D!=' 'and F==' ':C.append((B,E));B=E
			D=F
		if B<len(A):C.append((B,len(A)))
		return C
	def _derive_col_indexes(A,header_row=_A):0
	def read(B,reader_options):
		A=reader_options;B.reader_options=A;E=B._get_parsed_headers(B.origin.path)if A.has_header else _A;I=open(B.origin.path,'r',encoding=B.encoding);C=[]
		if A.column_indexes or A.column_widths:
			if A.column_indexes and A.column_widths:raise Exception('column_indexes and column_widths are exclusive.')
			if A.column_widths:
				logging.debug(f"Using column widths: {A.column_widths}");H=0
				for J in A.column_widths:C+=[(H,H+J)];H+=J
			else:logging.debug(f"Using column indexes: {A.column_indexes}");C=A.column_indexes
		else:logging.debug(f"Using auto derived column indexes.");N=B._get_first_data_line(B.origin.path);C=B._discover_col_idx_ralgin_spaces(N)
		logging.debug(f"Column indexes: {C}")
		if not C:raise Exception('No column indexes or widths provided, and no headers found to derive column indexes.')
		F=len(C);D=ColsDataset(cols_count=F,names=[f"Column {A+1}"for A in range(F)],numeric_col_indexes=[A for A in range(F)],data=[[]for A in range(F)])
		if E:D.names=E.data
		K=A.lines.start if A.lines and A.lines.start else _A;O=A.lines.end if A.lines and A.lines.end else _A;G=K or 0
		for L in islice(I,K,O):
			G+=1
			if B._ignore_line(L):continue
			if E:
				if E.ori_line_idx==G-1:continue
			for(P,M)in enumerate(C):Q=L[M[0]:M[1]].strip();R=string_2_float(Q);D.data[P].append(R)
			D.origin_line_nb.append(G)
		D.rows_count=len(D.origin_line_nb);I.close();B.cols_dataset=D;B.raw_lines_number=G;B.curves=_A;B.cols_curve=_A
		if A.curve_parser:
			if A.curve_parser.name==ReaderCurveParserNameConfig.COL_X:
				B.curves,S=cols_dataset_get_curves_col_x(D,A.curve_parser.parameters.x)
				if B.curves:B.cols_curve=ColsCurves(type=ReaderCurveParserNameConfig.COL_X,info=S,curves=B.curves)
			elif A.curve_parser.name==ReaderCurveParserNameConfig.COLS_COUPLE:raise NotImplementedError('cols_couple not implemented')
			else:raise Exception('Curve parser not supported.')
	def compare(A,compare_floats,param_reader,param_is_ref=True):D=param_is_ref;C=param_reader;B=compare_floats;E=A.cols_dataset if D else C.cols_dataset;F=A.cols_dataset if not D else C.cols_dataset;G=A.cols_curve;I,H=B.compare_errors.add_group('node','txt cols');return compare(H,B,E,F,G)
	def class_info(A):return{'cols':A.cols_dataset.names,'raw_lines_number':A.raw_lines_number,'curves':A.curves}