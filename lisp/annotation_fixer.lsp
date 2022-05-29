(vl-load-com)

(defun PTCC:fix-annotations (/ leaderList obj modelspace leaderObj)
	(setq modelspace (vla-get-ModelSpace (vla-get-ActiveDocument (vlax-get-acad-object))))
	(vlax-for obj modelspace
		(princ (strcat(vla-get-ObjectName obj) "\n"))
		(if (= (vla-get-ObjectName obj) "AcDbMLeader")
			(setq leaderList (append leaderList (list obj)))
		)
	)
	(foreach leaderObj leaderList
		(setq newLeaderObj (vla-Copy leaderObj))
		(vla-Delete leaderObj)
	)
)