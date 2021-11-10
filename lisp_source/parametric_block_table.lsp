(vl-load-com)

(defun C:linkBlockTable(/ ssParamBlocks paramBlock table tableReactor paramBlockReactor)
;; Description:
;; ===========
;; This function is the main entry point of the script.
;; It links the table and the parametric block and does some checkings if they fit for linking.
;; It checks if the table and parametric block are okay, it automatically syncs the table
;; from the parameteric block.
;;
;; Params:
;; =======
;; none
;;
;; Returns:
;; =======
;; none

	;; pick the parametric blocks
	(princ "\nPick parametric blocks to link: ")
	(setq ssParamBlocks (ssget '((0 . "INSERT"))))
	(princ "\n")
	(setq table (car (entsel "Pick the table:")))
	(setq PARTCOLNUM (findColNumber table "Part Name"))

	(if (> (sslength ssParamBlocks) 0)
		(repeat (setq i (sslength ssParamBlocks))
			(setq paramBlock (ssname ssParamBlocks (setq i (1- i))))
			(if (isTableBlockOK table paramBlock)
				(progn
					(if (not (isSync table paramBlock))
						(updateTable table paramBlock)
					)
					(setq tableReactor (vlr-object-reactor (list (vlax-ename->vla-object table))
															paramBlock 
															'((:vlr-modified . syncParametricBlock)))
					)
					(setq paramBlockReactor (vlr-object-reactor (list (vlax-ename->vla-object paramBlock))
																table
																'((:vlr-modified . syncTable)))
					)
				)
			)
		)
	)
  (princ)
)

(defun syncTable(paramBlock reactor args / table)
;; Description:
;; ============
;; This callback function is called when bricscad detects changes in the parametric block.
;; This will update the table according to the changes in the parametric block.
;;
;; Parameters:
;; ===========
;; paramBlock - VLA-OBJECT, this is the object the has been modified
;; reactor - VLA-REACTOR, this is the reactor object
;; args - LIST, list of arguments from the reactor callback function. (VLA-MODIFIED 0 args)
;;
;; Returns:
;; ========
;; none

	(setq paramBlock (vlax-vla-object->ename paramBlock))
	(setq table (vlr-data reactor))
	(if (not(isSync table paramBlock))
		(updateTable table paramBlock)
	)
)

(defun syncParametricBlock(table reactor args / paramBlock)
;; Description:
;; ============
;; This callback function is called when bricscad detects changes in the table.
;; This will update the parametric block according to the changes in the table.
;;
;; Parameters:
;; ===========
;; paramBlock - VLA-OBJECT, this is the object the has been modified
;; reactor - VLA-REACTOR, this is the reactor object
;; args - LIST, list of arguments from the reactor callback function. (VLA-MODIFIED 0 args)
;;
;; Returns:
;; ========
;; none

	(setq table (vlax-vla-object->ename table))
	(setq paramBlock (vlr-data reactor))
	(if (not(isSync table paramBlock))
		(updateBlock table paramBlock)
	)
)

(defun updateTable(table paramBlock / compName paramPairs partRowNum paramName paramVal paramColNum pair)
;; Description:
;; ============
;; This function updates the table parameter values based from the changes made in the parametric block.
;;
;; Parameters:
;; ===========
;; table - ENAME, the table
;; paramBlock - ENAME, the parametric block
;;
;; Returns:
;; ========
;; none

	(setq compName (bmlispget "ComponentName" (getComponentHandle paramBlock)))
	(setq paramPairs (getParamPairs paramBlock))
	(setq partRowNum (findRowNumber table compName PARTCOLNUM))
	(foreach pair paramPairs
		(setq paramName (car pair))
		(setq paramVal (cdr pair))
		(setq paramColNum (findColNumber table paramName))
		(vla-settext (vlax-ename->vla-object table) partRowNum paramColNum paramVal)
		(princ)
	)
)

(defun updateBlock(table paramBlock / compName paramPairs partRowNum paramName paramVal paramColNum pair)
;; Description:
;; ============
;; This function updates the values in the parametric block according to the changes made in the table.
;; For now this function modifies all parameters at once.
;;
;; Parameters:
;; ===========
;; table - ENAME, the table
;; paramBlock - ENAME, the parametric block
;;
;; Returns:
;; ========
;; none

	(setq compName (bmlispget "ComponentName" (getComponentHandle paramBlock)))
	(setq paramPairs (getParamPairs paramBlock))
	(setq partRowNum (findRowNumber table compName PARTCOLNUM))
	(foreach pair paramPairs
		(setq paramName (car pair))
		(setq paramVal (cdr pair))
		(setq paramColNum (findColNumber table paramName))
		(setq tableParamVal (vla-gettext (vlax-ename->vla-object table) partRowNum paramColNum))
		(command "_-BMPARAMETERS" paramBlock "" "Edit" paramName tableParamVal)
		(princ)
	)
)

(defun isSync(table paramBlock / compName paramPairs partRowNum paramName paramVal paramColNum synced pair)
;; Description:
;; ============
;; This function checks if the table and the parametric block are in synced. Synced means that the parameter values
;; in the parametric block are equal to the values in the table
;;
;; Parameters:
;; ===========
;; table - ENAME, the table
;; paramBlock - ENAME, the parametric block
;;
;; Returns:
;; ========
;; synced - T/-1, T if they are synced. -1 if they are not synced.

	(setq synced T)
	(setq compName (bmlispget "ComponentName" (getComponentHandle paramBlock)))
	(setq paramPairs (getParamPairs paramBlock))
	(setq partRowNum (findRowNumber table compName PARTCOLNUM))
	(foreach pair paramPairs
		(setq paramName (car pair))
		(setq paramVal (cdr pair))
		(setq paramColNum (findColNumber table paramName))
		(if (not (eq paramVal (atoi (vla-gettext (vlax-ename->vla-object table) partRowNum paramColNum))))
			(setq synced NIL)
		)
	)
  synced
)


(defun isTableBlockOK(table paramBlock / isOK partRowNum paramPairs found paramName paramVal pair paramColNum compName)
;; Description:
;; ============
;; This function checks some compatibility issues of the table and the parametric block.
;;
;; Parameters:
;; ===========
;; table - ENAME, the table
;; paramBlock - ENAME, the parametric block
;;
;; Returns:
;; ========
;; isOK - T/NIL (T if table and parametrics blocks does not have compatibility issues, NIL otherwise)

	(setq isOK T)
	(setq compName (bmlispget "ComponentName" (getComponentHandle paramBlock)))
	;; check if the "Part Name" Column is in the Columns of the table
	(if (= PARTCOLNUM -1)
		(progn
			(princ "Cannot find Part Name column\n")
			(setq isOK NIL)
		)
		(progn
			;; check if the Component Name is in the Table
			(setq partRowNum (findRowNumber table compName partColNum))
			(if (= partRowNum -1)
				(progn
					(princ "Cannot find Component Name in the Table\n")
					(setq isOK NIL)
				)
				(progn
					;; check if all the parameters are on the Columns of the Table
					(setq paramPairs (getParamPairs paramBlock))
					(setq found T)
					(foreach pair paramPairs
						(setq paramName (car pair))
						(setq paramVal (cdr pair))
						(setq paramColNum (findColNumber table paramName))
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

(defun getParamPairs(paramBlock / compHandle paramNames paramPairs paramVal paramName)
;; Description:
;; ============
;; This function gets the parameter names and it value from the parametric block and
;; group them as a list of dotted-pairs. example, (("LENGTH" . 15), ("WIDTH" . 20))
;;
;; Parameters:
;; ===========
;; paramBlock - ENAME, the parametric block.
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

(defun findColNumber(table colName / nCols currCol found colNumber)
;; Description:
;; ============
;; Finds the column number of the specified column name in the table
;;
;; Parameters:
;; ===========
;; table - ENAME, table to use for lookup.
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

(defun findRowNumber(table rowName colNumber / nRows found rowNumber currRow)
;; Description:
;; ============
;; Finds the row number given its rowName and colNumber in the table.
;;
;; Parameters:
;; ===========
;; table - ENAME, table to use for lookup.
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
