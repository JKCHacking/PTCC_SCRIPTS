; +--------------------------------+ 
; | Author: Joshnee Kim Cunanan    |
; | Version: 1                     |
; | Date: August 13, 2023          |
; +--------------------------------+

(vl-load-com)

(defun C:AutoLabel3 (/ acadObj viewPort )
  (if (/= 0 (getvar 'tilemode))
    (progn
      (princ "Error: You must be in paper space to run this script.")
      (exit)
    )
  )
  (setq acadObj (vlax-get-acad-object))
  (setq viewPort (getViewport))
  (princ (strcat "Handle: " (vla-get-handle viewPort)))
  (vla-put-activepviewport (vla-get-activedocument acadObj) viewPort)
  (command "mspace")
  (getUserInput viewPort (vla-get-paperspace (vla-get-activedocument acadObj)))
  (command "pspace")
  (princ)
)

(defun getBlocks (/ ssBlocks)
  (princ "Select one or more blocks.")
  (setq ssBlocks (ssget '((0 . "INSERT"))))
)

(defun getViewport (/ ss viewPort)
  (princ "Select a viewport.")
  (setq ss (ssget '((0 . "VIEWPORT"))))
  (setq viewPort (vlax-ename->vla-object (ssname ss 0)))
)

(defun getUserInput (viewPort paperSpace / mousePos retsel blockName leaderPt choice)
  ; ask the user to click on a block, 
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
            (setq mousePos (cadr retsel))
            (setq leaderPt (list (car mousePos) (cadr mousePos) 0))
            (addMLeader leaderPt blockName viewPort paperSpace)
          )
        )
      )
    )
    (setq choice (strcase (getstring "\nAdd more Mleaders? (y/n): ")))
    (if (or (= choice "n") (= choice "N"))
      (setq infiniteLoop NIL)
    )
  )
)

(defun addMLeader (leaderPt blockName viewPort paperSpace / landingPt pointList mleaderObj)
  (setq leaderPt (append (reverse (cdr (reverse (trans leaderPt 2 3)))) '(0)))
  (setq landingPt (calculateLandingPoint leaderPt viewPort))
  (setq pointList (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 5)) (append leaderPt landingPt)))  
  (setq mleaderObj (vla-AddMLeader paperSpace pointList 0))
  (vla-put-TextString mleaderObj blockName)
)

(defun calculateLandingPoint (leaderPt viewPort / minPt maxPt 
                                                  lowerLeft upperRight lowerRight upperLeft 
                                                  dist 
                                                  distUR distUL distLR distLL 
                                                  pairs minDist refPoint dir_angle
                                                  final_angle landingPt)
  (vla-GetBoundingBox viewPort 'minPt 'maxPt)
  (setq lowerLeft (vlax-safearray->list minPt)
	      upperRight (vlax-safearray->list maxPt)
        lowerRight (list (car upperRight) (cadr lowerLeft))
        upperLeft (list (car lowerLeft) (cadr upperRight))
        dist 10
        distUR (distance leaderPt upperRight)
        distUL (distance leaderPt upperLeft)
        distLR (distance leaderPt lowerRight)
        distLL (distance leaderPt lowerLeft)
        pairs (list (cons distUR upperRight) 
                    (cons distUL upperLeft) 
                    (cons distLR lowerRight) 
                    (cons distLL lowerLeft)
              )
        minDist (min distUR distUL distLR distLL)
        refPoint (cdr (assoc minDist pairs))
        dir_angle (rad2deg (angle leaderPt refPoint))
  )
  (princ (strcat "pairs: " (vl-princ-to-string pairs) "\n"))
  (princ (strcat "Nearest Point: " (vl-princ-to-string refPoint) "\n"))
  (princ (strcat "direction angle: " (rtos dir_angle) "\n"))
  (cond
    (
      (and (>= dir_angle 0) (<= dir_angle 90))
      (setq final_angle (deg2rad 45))
    )
    (
      (and (> dir_angle 90) (<= dir_angle 180))
      (setq final_angle (deg2rad 135))
    )
    (
      (and (> dir_angle 180) (<= dir_angle 270))
      (setq final_angle (deg2rad 225))
    )
    (
      (and (> dir_angle 270) (<= dir_angle 360))
      (setq final_angle (deg2rad 315))
    )
  )
  (princ (strcat "Final Angle: " (rtos final_angle) "\n"))
  (princ (strcat "Leader Point: " (vl-princ-to-string leaderPt) "\n"))
  (princ (strcat "Distance: " (rtos dist) "\n"))
  (setq landingPt (polar leaderPt final_angle dist))
  (princ (strcat "Landing Point: " (vl-princ-to-string landingPt) "\n"))
  landingPt
)

(defun deg2rad (degrees / )
  (/ (* pi degrees) 180)
)

(defun rad2deg (radians) 
  (* 180.0 (/ radians pi))
)
