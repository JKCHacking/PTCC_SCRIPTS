(vl-load-com)

(defun PTCC:ReposMleaders(/)
  (setq acadObj (vlax-get-acad-object))
  (setq doc (vla-get-ActiveDocument acadObj))
  (setq modelSpace (vla-get-ModelSpace doc))

  (vlax-for obj modelSpace
    (if (= (vla-get-ObjectName obj) "AcDbMLeader")
      (progn
        (princ (strcat "Name: " (vla-get-ObjectName obj) " Handle: " (vla-get-Handle obj) "\n"))
        (setq copyMLeaderObj (vla-Copy obj))
        (vla-Delete obj)
      )
    )
  )
)