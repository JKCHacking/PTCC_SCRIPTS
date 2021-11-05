(vl-load-com)

(defun C:linkBlockTable()
	(setq table (car (entset "Pick the table:")))
	(setq paramBlock (car (entset "Pick the Parametric Block:")))
	(setq compName (bmlispget "ComponentName" (getComponentHandle paramBlock)))
	(setq partColNum (findColNumber "Part Name"))
	(if (isTableBlockOK)
		(progn
			;; (setq tableReactor (vlr-object-reactor (list (vlax-ename->vla-object table)) NIL '((:vlr-modified . syncParametricBlock))))
			;; (setq paramBlockReactor (vlr-object-reactor (list (vlax-ename->vla-object paramBlock)) NIL '((:vlr-modified . syncTable))))
		)
	)
)

(defun T:testInit()
	(setq table (handent "123"))
	(setq paramBlock (handent "9B"))
	(setq compName (bmlispget "ComponentName" (getComponentHandle paramBlock)))
	(setq partColNum (findColNumber "Part Name"))
)

(defun T:testUpdateTable()
	(funcGroup "updateTable")
)
(defun T:testUpdateBlock()
	(funcGroup "updateBlock")
)
(defun T:testIsSync()
	(funcGroup "isSync")
)
(defun T:testIsTableBlockOK()
	(isTableBlockOK)
)

(defun syncTable()
	(if (not (funcGroup "isSync"))
		(funcGroup "updateTable")
	)
)

(defun syncParametricBlock()
	(if (not (funcGroup "isSync"))
		(funcGroup "updateBlock")
	)
)

(defun funcGroup(funcName / paramPairs synced partRowNum paramName paramVal pair tableParamVal)
	(setq synced T)
	(setq paramPairs (getParamPairs))
	(setq partRowNum (findRowNumber compName partColNum))
	(foreach pair paramPairs
		(setq paramName (car pair))
		(setq paramVal (cdr pair))
		(setq paramColNum (findColNumber paramName))
		(cond
			((= funcName "updateTable")
				(vla-settext (vlax-ename->vla-object table) partRowNum paramColNum paramVal)
				(princ)
			)
			((= funcName "updateBlock")
				(setq tableParamVal (vla-gettext (vlax-ename->vla-object table) partRowNum paramColNum))
				(command "_-BMPARAMETERS" paramBlock "" "Edit" paramName tableParamVal)
				(princ)
			)
			((= funcName "isSync")
				;; check if the parameter value is not equal to the current value in the table.
				;; if not then they are not synced.
				(cond
					((not (eq paramVal (atoi (vla-gettext (vlax-ename->vla-object table) partRowNum paramColNum))))
						(setq synced NIL)
					)
				)
				synced
			)
		)
	)
)

(defun isTableBlockOK(/ isOK partRowNum paramPairs found paramName paramVal pair paramColNum)
	(setq isOK T)
	;; check if the "Part Name" Column is in the Columns of the table
	(if (= partColNum -1)
		(progn
			(princ "Cannot find Part Name column\n")
			(setq isOK NIL)
		)
		(progn
			;; check if the Component Name is in the Table
			(setq partRowNum (findRowNumber compName partColNum))
			(if (= partRowNum -1)
				(progn
					(princ "Cannot find Component Name in the Table\n")
					(setq isOK NIL)
				)
				(progn
					;; check if all the parameters are on the Columns of the Table
					(setq paramPairs (getParamPairs))
					(setq found T)
					(foreach pair paramPairs
						(setq paramName (car pair))
						(setq paramVal (cdr pair))
						(setq paramColNum (findColNumber paramName))
						(if (= paramColNum -1)
							(setq found NIL)
						)
					)
					(if (not found)
						(progn
							(princ "There are missing parameters in the Table\n")
							(setq isOK NIl)
						)
					)
				)
			)
		)
	)
	isOK
)

(defun getParamPairs( / compHandle paramNames paramPairs paramVal paramName)
	(setq compHandle (getComponentHandle paramBlock))
	(setq paramNames (bmlispget "Parameters" compHandle))
	(setq paramPairs ())
	(foreach paramName paramNames
		(setq paramVal (bmlispget "ParameterValue" compHandle paramName))
		(setq paramPairs (append paramPairs (list (cons paramName paramVal))))
	)
	paramPairs
)

(defun getComponentHandle (ent / componentList componentHandle thisComp asmList thisInstance)
	(setq componentList (bmlispget "Components"))
	(foreach thisComp componentList
		(cond
			((bmlispget "IsAssembly" thisComp)
				(setq asmList (bmlispget "Instances" thisComp))
				(foreach thisInstance asmList
					(cond
						((eq ent (bmlispget "BlockReference" thisInstance))
							(setq componentHandle (bmlispget "Component" thisInstance))
						)
					)
				)
			)
		)
	)
	componentHandle
)

(defun findColNumber(colName / nCols currCol found colName colNumber)
	(setq nCols (vla-get-columns (vlax-ename->vla-object table)))
	(setq currCol 0)
	(setq found NIL)
	(while (and (< currCol nCols) (not found))
		(if (= colName (vla-gettext (vlax-ename->vla-object table) 0 currCol))
			(progn
				(setq found T)
				(setq colNumber currCol)
			)
		)
		(setq currCol (+ currCol 1))
	)

	(if (not found)
		(setq colNumber -1)
	)
	colNumber
)

(defun findRowNumber(rowName colNumber / nRows found rowNumber currRow)
	(setq nRows (vla-get-rows (vlax-ename->vla-object table)))
	(setq currRow 1)
	(setq found NIL)
	;; find row number of the partname by looping in the part name column.
	(while (and (< currRow nRows) (not found))
		(if (= rowName (vla-gettext (vlax-ename->vla-object table) currRow colNumber))
			(progn
				(setq found T)
				(setq rowNumber currRow)
			)
		)
		(setq currRow (+ currRow 1))
	)

	(if (not found)
		(setq rowNumber -1)
	)
	rowNumber
)
