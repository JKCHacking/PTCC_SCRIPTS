(defun c:test_script (/ ss vlobject val) 
  (setq ss (ssget "X" '((0 . "ACAD_TABLE"))))
  (setq vlobject (vlax-ename->vla-object (ssname ss 0)))

  (setq val (vlax-variant-value (vla-GetCellValue vlobject 1 0)))
  (print val)
)

(defun c:Test (/ doc objs) 
  ;;    Tharwat 10. Apr. 2014        ;;
  (cond 
    ((eq (getvar 'ctab) "Model")
     (princ "\n ** Command is not allowed in Model Space !!")
    )
    (t
     (vlax-for x 
               (vla-get-paperspace 
                 (setq doc (vla-get-activedocument 
                             (vlax-get-acad-object)
                           )
                 )
               )
               (if 
                 (and (/= (vla-get-objectname x) "AcDbViewport") 
                      (eq (vla-get-layer x) [color=magenta] "Layer1" [/color])
                 )
                 (setq objs (cons x objs))
               )
     )
     (if objs 
       (vlax-invoke 
         doc
         'CopyObjects
         objs
         (vla-get-ModelSpace doc)
       )
     )
    )
  )
  (princ)
)

(defun c:test2 (/ x) 
  (setq x (vla-get-Modelspace 
            (setq doc (vla-get-activedocument 
                        (vlax-get-acad-object)
                      )
            )
          )
  )
  (print x)
)

(defun c:test3 (/ x) 
  (setq x (getvar 'ctab))

  (print x)
)

(defun c:test4 ( / ss exdata entity parameter_name)
  (regapp "TEST4")
  (setq entity (entget(handent "D4B32")))
  (setq parameter_name "MM-05")
  
  (setq exdata (list (list -3 (list "TEST4" (cons 1000 parameter_name)))))
  (setq entity (append entity exdata))
  (entmod entity)
  
  (setq ss (ssget "X" '((-3 ("TEST4")))))
  (princ)
)

(c:test2)