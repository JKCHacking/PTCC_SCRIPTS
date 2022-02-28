(vl-load-com)

(defun PTCC:FixMleaders(/)
  (setq acadObj (vlax-get-acad-object))
  (setq doc (vla-get-ActiveDocument acadObj))
  (setq modelSpace (vla-get-ModelSpace doc))

  (vlax-for obj modelSpace
    (if (= (vla-get-ObjectName obj) "AcDbMLeader")
      (progn
        (princ (strcat "Name: " (vla-get-ObjectName obj) " Handle: " (vla-get-Handle obj) "\n"))
        (vla-GetBoundingBox obj 'minPt 'maxPt)
        (vla-Move obj minPt (vlax-3d-point 0 0 0))
        (vla-Move obj (vlax-3d-point 0 0 0) minPt)
      )
    )
  )
)