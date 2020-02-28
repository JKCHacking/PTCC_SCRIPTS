; Author: Joshnee Kim B. Cunanan
; FileName: adaptive_label_approach_1.lsp
; Date Modified: 21 Feb 2020
; Function: This script updates the table according to the parametric user input value.

; Desc: MAIN FUNCTION
; param: None
; local: parameter_name, new_length
; return: integer (Not used)
(defun c:main(/ parameter_name new_length)
  (setq parameter_name (getstring "\nSelect a parametric constraint: "))
  (setq new_length (getreal "\nEnter new length: "))
  
  (init)
  (modifylabelbyconstraints parameter_name new_length)
  (princ)
) 

; Desc: calls all iniatialization functions
; param: None
; local: None
; return: nil
(defun init()
  (print "init")
  (vl-load-com)
  (princ)
)

; Desc: Wrapper function for modifying parameter constraints and value in the table
; param: parameter_name, new_length
; local: None
; return: integer (Not used)
(defun modifylabelbyconstraints(parameter_name new_length)
  ; modify the value of the parametric constraints
  (modify_parameter_constraint parameter_name new_length)
  
  ; modifying the label name in the table according to the changes made.
  (modifytablecell parameter_name new_length)
  (princ)
)


; Desc: modifies the parametric constraints
; param: None
; local: parameter_name, new_length
; return: entity data
(defun modify_parameter_constraint(parameter_name new_length / entity_data ss i n dim_label en directX_obj new_length_str)
  (setq new_length_str (rtos new_length))
  (if (setq ss (ssget "X" '((8 . "*ADSK_CONSTRAINTS"))))
    (progn
      (setq i 0
            n (sslength ss)
      )
  
      (while (< i n)
        (setq en (ssname ss i)
              directX_obj (vlax-ename->vla-object en)
              dim_label (vlax-get-property directX_obj 'TextOverride)
        )
        
        (if (/= (vl-string-search parameter_name dim_label) nil)
            (progn
              ; cannot modify Meausrement property of text Measurement(RO)
              ;(vlax-put-property directX_obj 'Measurement new_length)
              
              ; approach 1:
              ; use vlf-comd to change the parameteric variable
              (vl-cmdf)
              (vl-cmdf "-PARAMETERS" "edit" parameter_name new_length_str "")
              (vl-cmdf)
            )
        )
        (setq i (1+ i))
      )
      (print entity_data)
    )
  )
)

; Desc: Modifies the value in the table cell.
; param: parameter_name, new_length
; local: ss, vlobjecttable, row, col, irow, icol, codecolumnindex, lencolumnindex, cellname, new_length_str
; return: integer (Not used)
(defun modifytablecell(parameter_name new_length / ss vlobjecttable row col irow icol codecolumnindex lencolumnindex cellname new_length_str)
  (setq ss (ssget "X" '((0 . "ACAD_TABLE"))))
  (setq vlobjecttable (vlax-ename->vla-object (ssname ss 0)))
  
  (setq row (vla-get-Rows vlobjecttable))
  (setq col (vla-get-Columns vlobjecttable))
  (setq irow 0)
  (setq icol 0)
  (setq codecolumnindex (getcolumnindex row col "Code" vlobjecttable))
  (setq lencolumnindex (getcolumnindex row col "Length" vlobjecttable))
  (setq new_length_str (rtos new_length))
  (setq found_flag 0)
  
  (while (< irow row)
    (setq cellname (vlax-variant-value (vla-GetCellValue vlobjecttable irow codecolumnindex)))
    (if (= cellname parameter_name)
      (progn
        (vla-SetText vlobjecttable irow lencolumnindex new_length_str)
        (setq found_flag 1)
      )
    )
    (setq irow (1+ irow))
  )
  
  (if (= found_flag 0)
    (print "Parameter Name not found!")
  )
  
  (princ)
)

; Desc: gets the column index of the specific column desired.
; param: row, col, headername vlobjecttable
; local: irow, icol, headercolumnindex, cellname
; return: integer (Not used)
(defun getcolumnindex(row col headername vlobjecttable / irow icol headercolumnindex cellname)
  (setq irow 0)
  (setq icol 0)
  (setq headercolumnindex 0)
  
  (while (< icol col)
    ; get the value of the header
    (setq cellname (vlax-variant-value (vla-GetCellValue vlobjecttable 0 icol)))
    (if (= cellname headername)
      (setq headercolumnindex icol)
    )
    (setq icol (1+ icol))
  )
  
  (print headercolumnindex)
)

(c:main)

;================================== UNUSED CODES=====================================
;(defun add_extended_data(entity parameter_name / exdata)
;  (setq exdata (list (list -3 (list "EXTENDED_DATA2" (cons 1000 parameter_name)))))
;  (setq entity (append entity exdata))
;  (entmod entity)
;)

;(defun modify_attribute (new_value en code_group / entity_data)
;  (if (= code_group 1)
;    (setq new_value(rtos new_value))
;  )
;  
;  (setq entity_data (entget en))
;  (setq entity_data 
;        (subst (cons code_group new_value)
;               (assoc code_group entity_data) 
;                entity_data
;        )
;  )
;  
;  (entmod entity_data)
;)

;  (regapp "EXTENDED_DATA2")
;  
;  ;add extended data
;  (setq e_lower_side (entget(handent "7B")))
;  (setq e_upper_side (entget(handent "7D")))
;  (setq e_right_side (entget(handent "7E")))
;  (setq e_left_side (entget(handent "7C")))
;  
;  (add_extended_data e_lower_side "lower_side")
;  (add_extended_data e_upper_side "upper_side")
;  (add_extended_data e_right_side "right_side")
;  (add_extended_data e_left_side "left_side")