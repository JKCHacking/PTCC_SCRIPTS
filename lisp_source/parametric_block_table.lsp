(vl-load-com)

(defun C:linkBlockTable()
	(setq table (handent "123"))
	(setq paramBlock (handent "9B"))
	;; (setq tableReactor (vlr-object-reactor (list (vlax-ename->vla-object table)) NIL '((:vlr-modified . syncParametricBlock))))
	(setq paramBlockReactor (vlr-object-reactor (list (vlax-ename->vla-object paramBlock)) NIL '((:vlr-modified . syncTable))))
	;; (setq compName (GetComponentName paramBlock))
)

(defun syncTable(paramBlk rtr arg / ename compHandle paramNames paramPairs paramVal)
	; get the parameters as list of dotted-pair
	(setq enameParamblk (vlax-vla-object->ename paramBlk))
    (setq compHandle (getComponentHandle enameParamblk))
	(setq paramNames (bmlispget "Parameters" compHandle))
	(setq paramPairs ())
	(foreach paramName paramNames
		(setq paramVal (bmlispget "ParameterValue" compHandle paramName))
		(setq paramPairs (append paramPairs (list (cons paramName paramVal))))
	)
	(updateTable compHandle paramPairs)
)

(defun updateTable(compHandle paramPairs / nRows currRow compName 
	partColNum paramColNum paramName paramVal pair)
	(setq nRows (vla-get-rows (vlax-ename->vla-object table)))
	(setq currRow 1)
	(setq compName (bmlispget "ComponentName" compHandle))
	(setq partColNum (findColNumber "Part Name"))
	(if (= partColNum -1) 
		(princ "Cannot find Part Name column") 
		(progn
			(while (< currRow nRows)
				;; find row number of the partname by looping in the part name column.
				(cond 
					((= compName (vla-gettext (vlax-ename->vla-object table) currRow partColNum))
						(foreach pair paramPairs
							(setq paramName (car pair))
							(setq paramVal (cdr pair))
							(setq paramColNum (findColNumber paramName))
							(cond
								;; dont modify if the cell value have not changed. or the parameter value 
								;; is not equal to the current value in the table.
								((not (eq paramVal (vla-gettext (vlax-ename->vla-object table) currRow paramColNum)))
									(vla-settext (vlax-ename->vla-object table) currRow paramColNum paramVal)
								)
							)
						)
					)
				)
				(setq currRow (+ currRow 1))
			)
		)
	)
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

(defun findColNumber(colName / nCols currCol)
	(setq nCols (vla-get-columns (vlax-ename->vla-object table)))
	(setq currCol -1)
	(while (and (< currCol nCols) (not (= colName (vla-gettext (vlax-ename->vla-object table) 0 currCol))))
		(setq currCol (+ currCol 1))
	)
	currCol
)