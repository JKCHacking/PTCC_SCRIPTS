(vl-load-com)

(defun C:linkBlockTable()
;; Description:
;; ===========
;; This function is the main entry point of the script.
;; It links the table and the parametric block and does some checkings if they fit for linking.
;; It checks if the table and parametric block are okay, it automatically syncs the table
;; from the parameteric block. right now it only accepts 1:1 relationship between 
;; a parametric block and a table.
;;
;; Params:
;; =======
;; none
;;
;; Returns:
;; =======
;; none

	(setq table (car (entsel "Pick the table:")))
	(setq paramBlock (car (entsel "Pick the Parametric Block:")))
	(setq compName (bmlispget "ComponentName" (getComponentHandle paramBlock)))
	(setq partColNum (findColNumber "Part Name"))
	(if (isTableBlockOK)
		(progn
      (if (not (funcGroup "isSync"))
          (funcGroup "updateTable")
      )
			(setq tableReactor (vlr-object-reactor (list (vlax-ename->vla-object table)) NIL '((:vlr-modified . syncParametricBlock))))
			(setq paramBlockReactor (vlr-object-reactor (list (vlax-ename->vla-object paramBlock)) NIL '((:vlr-modified . syncTable))))
		)
	)
)

;; ====================================TESTING FUNCTIONS======================================
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
;; =======================================END=====================================================

(defun syncTable()
;; Description:
;; ============
;; This callback function is called when bricscad detects changes in the parametric block.
;; This will update the table according to the changes in the parametric block.
;;
;; Parameters:
;; ===========
;; none
;;
;; Returns:
;; ========
;; none

	(if (not (funcGroup "isSync"))
		(funcGroup "updateTable")
	)
)

(defun syncParametricBlock()
;; Description:
;; ============
;; This callback function is called when bricscad detects changes in the table.
;; This will update the parametric block according to the changes in the table.
;;
;; Parameters:
;; ===========
;; none
;;
;; Returns:
;; ========
;; none

	(if (not (funcGroup "isSync"))
		(funcGroup "updateBlock")
	)
)

(defun funcGroup(funcName / paramPairs synced partRowNum paramName paramVal pair tableParamVal)
;; Description:
;; ============
;; This function contains different subfunctions.
;; *very ugly, iknow. right now i cant think of other solution in this language.*
;;
;; Parameters:
;; ===========
;; funcName - STR, name of the subfunctions to be called:
;;            updateTable - will update the cell in the table
;;            updateBlock - will update the parameters in the parametric block
;;            isSync - checks if the parametric block and the table are not in synced. synced means
;;            that the parameters of the parametric block does not equal to the parameters in the table.
;;
;; Returns:
;; ========
;; If funcName is either "updateBlock" or "updateTable":
;; none
;; If funcName is isSync:
;; synced - T or -1. T means that the parametric block and table are in synced.
;;          -1 means that the parametrick and table are not in synced.

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
;; Description:
;; ============
;; This function checks some compatibility issues of the table and the parametric block.
;;
;; Parameters:
;; ===========
;; none
;;
;; Returns:
;; ========
;; isOK - T/NIL (T if table and parametrics blocks does not have compatibility issues, NIL otherwise)

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
							(setq isOK NIL)
						)
					)
				)
			)
		)
	)
	isOK
)

(defun getParamPairs( / compHandle paramNames paramPairs paramVal paramName)
;; Description:
;; ============
;; This function gets the parameter names and it value from the parametric block and
;; group them as a list of dotted-pairs. example, (("LENGTH" . 15), ("WIDTH" . 20))
;;
;; Parameters:
;; ===========
;; none
;;
;; Returns:
;; ========
;; paramPairs - list of dotted-pairs of parameter name and value.

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
;; Description:
;; ============
;; Gets the component handle number of the parametric block.
;;
;; Parameters:
;; ===========
;; ent - ENAME, parametric block
;;
;; Returns:
;; componentHandle - STR, handle of the component in the parametric block.

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
;; Description:
;; ============
;; Finds the column number of the specified column name in the table
;;
;; Parameters:
;; ===========
;; colName - STR, column name to find its column number
;;
;; Returns:
;; ========
;; colNumber - INT, column number of the specified column name.

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
;; Description:
;; ============
;; Finds the row number given its rowName and colNumber in the table.
;;
;; Parameters:
;; ===========
;; rowName - STR, row name
;; colNumber - INT, column number
;;
;; Returns:
;; ========
;; rowNumber - INT, row number

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
