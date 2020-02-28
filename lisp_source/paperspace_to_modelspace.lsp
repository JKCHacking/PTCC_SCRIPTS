; Author: Joshnee Kim Cunanan
; Date: 26 Feb 2020

; global
(setq *app-name* "PAPERSPACE_TO_MODELSPACE")

(defun c:paper-space-to-model-space (/ paper-space-info paper-space-object)  
  (setq paper-space-info(get-space-info "Paper Space")
        new-length "2000 MM."
        parameter-name "MM-01"
  )
  (init)
  (modify-parameter-constraints parameter-name new-length)
  (modify-text-table parameter-name new-length)
)

(defun init()
  (regapp *app-name*)
  (vl-load-com)
  
  ; attaching extended data on a text in a table
  (setq mm-01-object (entget(handent "D4B32")))
  (add-extended-data mm-01-object "MM-01")
  (princ)
)

(defun modify-text-table(parameter-name new-length / filtered-ss)
  (if(setq filtered-ss (ssget "X" (list(list -3 (list *app-name* (cons 1000 parameter-name))))))
      (progn
        (setq i 0)
        (while (setq object (ssname filtered-ss i))
          (modify-attribute new-length object 1)
          (setq i (1+ i))
        )
      )  
  )
  (princ)
)

(defun modify-parameter-constraint(parameter_name new_length / entity_data ss i n dim_label en directX_obj new_length_str)
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

(defun modify-attribute (new-value en code-group / entity-data)
  ; (if (= code-group 1)
  ;   (setq new-value(rtos new-value))
  ; )
  
  (setq entity-data (entget en))
  (setq entity-data 
        (subst (cons code-group new-value)
                (assoc code-group entity-data) 
                entity-data
        )
 )
  (entmod entity-data)
  (princ)
)

(defun add-extended-data(entity parameter_name / exdata)
 (setq exdata (list (list -3 (list *app-name* (cons 1000 parameter_name)))))
 (setq entity (append entity exdata))
 (entmod entity)
)

(defun get-space-info(space-option / space-objects)
    (if (= space-option "Model Space")
        (setq space-objects
               (get-model-space)
        )
      (if (= space-option "Paper Space")
        (setq space-objects 
               (get-paper-space)
        )
      )
    )
)

(defun get-model-space()
  ; get modelspace
  (setq space-objects  
        (vla-get-modelspace
            (setq doc 
                   (vla-get-activedocument 
                     (vlax-get-acad-object)
                   )
            )
        )
  )
)

(defun get-paper-space()
  ; get paperspace
  (setq space-objects  
        (vla-get-paperspace
            (setq doc 
                   (vla-get-activedocument 
                     (vlax-get-acad-object)
                   )
            )
        )
  )
)

(c:paper-space-to-model-space)