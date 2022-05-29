(vl-load-com)

(defun c:DumpDynProps (/ ss oDynProps)
  (if (and (setq ss (ssget "X"))
           (setq oDynProps (car (vlax-invoke
                                  (vlax-ename->vla-object (ssname ss 0))
                                  '(vla-GetDynamicBlockProperties)
                                )
                           )
           )
      )
    (progn (vlax-dump-object oDynProps T) (textpage))
    (prompt "\n** Invalid selection ** ")
  )
  (princ)
)

(c:DumpDynProps)