; +--------------------------------+ 
; | Author: Joshnee Kim Cunanan    |
; | Version: 1                     |
; | Date: July 25, 2023            |
; +--------------------------------+

(vl-load-com)

(defun C:AutoLabel2 (/ ssBlocks)
  (setq acadObj (vlax-get-acad-object))

  (setq ssBlocks (getBlocks))
  (if (/= ssBlocks NIL)
    (progn
      (zoomView acadObj ssBlocks)
    )
  )
)

(defun getBlocks (/ ssBlocks)
  (princ "Select one or more blocks...")
  (setq ssBlocks (ssget '((0 . "INSERT"))))
)

(defun attachMLeaderUser (modelSpace blockVla view / mousePos retsel blockName )
  ; change the color of the current block to a gradiaent color
  ; ask the user to click on the current block, 
  ; dont allow to click on other blocks
  (setq infiniteLoop T)
  (while infiniteLoop
    (setq retsel (entsel "Choose the leader point around the block.\n" ))
    (if (= retsel NIL)
      (princ "Please click around the block object!")
      (progn
        ; check if the user selected is a block
        (if (/= (cdr (assoc 0 (entget (car retsel)))) "INSERT")
          (progn
            (princ "This object is not a block!")
            (princ)
          )
          (progn
            (setq blockName (cdr (assoc 2 (entget (car retsel)))))
            (if (= blockName (vla-get-name blockVla))
              (progn
                (setq mousePos (cadr retsel))
                (setq infiniteLoop NIL)
              )
              (progn
                (princ (strcat "Incorrect block! choose blockname: " (vla-get-name blockVla)))
                (princ)
              )
            )
          )
        )
      )
    )
  )
  ; add the Mleader using the current mouse position as the leader point.
  ; assume a landing point. let the user adjust later after generation.
  (addMLeader modelSpace mousePos (vla-get-name blockVla) view)
  (princ)
)

(defun deg2rad (degrees / )
  (/ (* pi degrees) 180)
)

(defun zoomView (acadObj ssBlocks / v bb minPt maxPt 
                 min_x min_y min_z max_x max_y max_z
                 lowerLeft upperRight)

  (setq views (list "top" "right" "front"))
  (foreach v views
    (princ (strcat "Change view to " v " view."))
    (command "-view" v)
    (princ "\n")
    (setq bb (getBBMulti ssBlocks)
          minPt (car bb)
          maxPt (cadr bb)
          min_x (car minPt)
          min_y (cadr minPt)
          min_z (caddr minPt)
          max_x (car maxPt)
          max_y (cadr maxPt)
          max_z (caddr maxPt)
    )
    (cond
      ((equal v "top")
       (setq lowerLeft (list min_x min_y 0)
            upperRight (list max_x max_y 0)
       )
      )
      ((equal v "right")
       (setq lowerLeft (list 0 min_y min_z)
            upperRight (list 0 max_y max_z)
       )
      )
      ((equal v "front")
       (setq lowerLeft (list min_x 0 min_z)
            upperRight (list max_x 0 min_z)
       )
      )
    )
    (vla-ZoomWindow acadObj (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 2)) lowerLeft) 
                    (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 2)) upperRight))
    (setq i 0)
    (while (setq blockEname (ssname ssBlocks i))
      (setq blockVla (vlax-ename->vla-object blockEname))
      (princ (strcat "Object to select: " (vla-get-name blockVla)))
      (attachMLeaderUser (vla-get-ModelSpace (vla-get-ActiveDocument acadObj)) blockVla v)
      (setq i (1+ i))
    )
  )
)

(defun getBBMulti (ssBlocks / i list_x list_y list_z 
                   blockEname vlObj 
                   minPt maxPt 
                   min_x min_y min_z 
                   max_x max_y max_z bb)
  (setq i 0)
  (setq list_x NIL 
        list_y NIL 
        list_z NIL)
  (while (setq blockEname (ssname ssBlocks i))
    (setq vlObj (vlax-ename->vla-object blockEname))
    (vla-GetBoundingBox vlObj 'minPt 'maxPt)
    (setq minPt (vlax-safearray->list minPt))
    (setq maxPt (vlax-safearray->list maxPt))
    
    ; min
    (setq list_x (cons (car minPt) list_x))
    (setq list_y (cons (cadr minPt) list_y))
    (setq list_z (cons (caddr minPt) list_z))
    ; max
    (setq list_x (cons (car maxPt) list_x))
    (setq list_y (cons (cadr maxPt) list_y))
    (setq list_z (cons (caddr maxPt) list_z))

    (setq i (1+ i))
  )
  
  ; get the most min point from all points
  (setq min_x (apply 'min list_x))
  (setq min_y (apply 'min list_y))
  (setq min_z (apply 'min list_z))
  ; get the most max point from all points
  (setq max_x (apply 'max list_x))
  (setq max_y (apply 'max list_y))
  (setq max_z (apply 'max list_z))
  (setq bb (list (list min_x min_y min_z) (list max_x max_y max_z)))
)

(defun addMLeader (modelSpace userPosition text view / mleaderObj
                                                        points
                                                        pointList)
  
  ;; (setq points (vlax-make-safearray vlax-vbDouble '(0 . 5)))
  ;; (setq pointList (append leaderPt landingPt))
  ;; (vlax-safearray-fill points pointList)
  (setq point1 (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 2)) (list 0 0 0))
        point2 (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 2)) (list 1 0 0))
        point3 (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 2)) (list 0 1 0))
        pointList (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 5)) (list 0 0 0 10 10 0))
        userPosition_sa (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 2)) userPosition)
  )
  
  (setq rotAngle (deg2rad 90))
  
  (setq mleaderObj (vla-AddMLeader modelSpace pointList 0))
  (vla-put-TextString mleaderObj text)
  ; rotate the mleader
  (cond
    (
      (equal view "top") 
      ()
    ) ; no need for rotate in top
    (
      (equal view "front")
      (vla-rotate3d mleaderObj point1 point2 rotAngle)
    )
    (
      (equal view "right")
      (vla-rotate3d mleaderObj point1 point3 rotAngle)
      (vla-rotate3d mleaderObj point1 point2 rotAngle)
    )
  )
  ; move the mleader to the user position
  (vla-move mleaderObj point1 userPosition_sa)
  (princ)
)