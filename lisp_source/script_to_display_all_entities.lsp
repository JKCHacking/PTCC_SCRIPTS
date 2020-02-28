(vl-load-com)

(defun c:test1 ( / modified_entity entity_extended en ss ptx pty new_dist)
  ;======================Draftsman work ====================================
  ; add extended data to LINE upper_side of the square and 
  ; to the MTEXT that points to the LINE upper_side.
  (setq entity_upper_side (entget(handent "7D")))
  (setq entity_text_dimension (entget(handent "9B")))
  ;  (setq en_lower_side (entget(handent "7B")))
  
  (regapp "EXTENDED_DATA2")
  (add_extended_data entity_upper_side)
  (add_extended_data entity_text_dimension)
  
  ;======================= this is a separate scenario =====================
  
  ; set temporary local variable for new point.
  (setq new_point (list 3.0 5.0 0))

  ; get the line using the extended data  
  (setq ss (ssget "X" '((0 . "LINE")(-3 ("EXTENDED_DATA2" (1000 . "upper_side"))))))
  (setq en (ssname ss 0))
  
  ; this is the part of changing the length of the line.
  ; for now it uses the point system.
  ; we can use to update the length of the line using parametric values
  
;  (setq modified_entity (modify_attribute new_point en 11))
;  (setq entity_extended(add_extended_data modified_entity))

  (setq pt1 (cdr(assoc 10 entget(en))))
  (setq pt2 (cdr(assoc 11 entget(en))))
  
  (setq modified_entity (modify_parameter_constraint "upper_side" 10 pt1 pt2))
  (setq entity_extended(add_extended_data modified_entity))
  
  (setq ptx (cdr(assoc 10 entity_extended)))
  (setq pty (cdr(assoc 11 entity_extended)))
  (setq new_dist (distance ptx pty))
  
  (setq ss (ssget "X" '((0 . "MTEXT")(-3 ("EXTENDED_DATA2" (1000 . "upper_side"))))))
  (setq en (ssname ss 0))
  (setq modified_entity (modify_attribute new_dist en 1))
  (setq entity_extended(add_extended_data modified_entity))
  (princ)
)

(defun modify_attribute (new_value en code_group / entity_data)
  (if (= code_group 1)
    (setq new_value(rtos new_value))
  )
  
  (setq entity_data (entget en))
  (setq entity_data 
        (subst (cons code_group new_value)
               (assoc code_group entity_data) 
                entity_data
        )
  )
  
  (entmod entity_data)
)

(defun modify_parameter_constraint(parameter_name new_length pt1 pt2 / entity_data ss i n dim_label en directX_obj)
  ; possible parameters:
  ;       substring
  ;       new_length
  ; search for the whole selection set that are in layer "*ADSK_CONSTRAINTS".
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
;              (vlax-dump-object directX_obj)
                ; cannot modify Meausrement property of text
;              (vlax-put-property directX_obj 'Measurement new_length)
              
            )
        )
        (setq i (1+ i))
      )
      (print entity_data)
    )
  )
  ; check if theres a substring in the TextOverride property
  ; get the entity name
  ; set a new value in Measurement property
)


(defun add_extended_data(entity / exdata app_name)
  (setq exdata '((-3 ("EXTENDED_DATA2" (1000 . "upper_side")))))
  (setq entity (append entity exdata))
  (entmod entity)
)

(defun get_new_point(pt1 ang dist)
  
)

(c:test1)