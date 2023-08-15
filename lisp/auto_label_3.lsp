; +--------------------------------+ 
; | Author: Joshnee Kim Cunanan    |
; | Version: 1                     |
; | Date: August 13, 2023            |
; +--------------------------------+

(vl-load-com)

(defun C:AutoLabel3 (/)
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

(defun getUserInput (viewPort paperSpace / mousePos retsel blockName )
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

(defun addMLeader (leaderPt blockName viewPort paperSpace /)
  (setq landingPt (calculateLandingPoint leaderPt viewPort))
  (setq leaderPt_ps (append (reverse (cdr (reverse (trans leaderPt 2 3)))) '(0)))
  (setq landingPt_ps (append (reverse (cdr (reverse (trans landingPt 2 3)))) '(0)))
  (setq pointList (vlax-safearray-fill (vlax-make-safearray vlax-vbDouble '(0 . 5)) (append leaderPt_ps landingPt_ps)))
  (setq mleaderObj (vla-AddMLeader paperSpace pointList 0))
  (vla-put-TextString mleaderObj blockName)
)

(defun calculateLandingPoint (leaderPt viewPort /)
  (vla-GetBoundingBox viewPort 'minPt 'maxPt)
  (setq lowerLeft (vlax-safearray->list minPt)
	      upperRight (vlax-safearray->list maxPt))
  (setq x_min (min (car lowerLeft) (car upperRight)))
  (setq y_min (min (cadr lowerLeft) (cadr upperRight)))
  (setq dir_angle (rad2deg (angle leaderPt (list x_min y_min))))
  (setq dist 10)
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
  (setq landingPt (list 
                    (+ (car leaderPt) (* dist (cos final_angle))) 
                    (+ (cadr leaderPt) (* dist (sin final_angle))) 
                    0
                  )
  )
)

(defun deg2rad (degrees / )
  (/ (* pi degrees) 180)
)

(defun rad2deg (radians) 
  (* 180.0 (/ radians pi))
)
