(vl-load-com)

(defun C:AutoBlockLabel( / leaderLineLen 
                           landingLineLen 
                           acadObj 
                           doc 
                           modelSpace 
                           ssBlocks 
                           block 
                           block_vla 
                           i 
                           minExt 
                           maxExt
                           botLeftPt
                           topRightPt
                           midPoints
                           point
                           landingPt
                           rightMid leftMid topMid botMid)

    (setq leaderLineLen (getreal "Enter the Leader Line Length: "))
    (setq landingLineLen (getreal "Enter the Landing Line Length: "))
    (setq acadObj (vlax-get-acad-object))
    (setq doc (vla-get-ActiveDocument acadObj))
    (setq modelSpace (vla-get-ModelSpace doc))

    (setq ssBlocks (ssget "A" '((0 . "INSERT"))))
    (if (> (sslength ssBlocks) 0)
        (repeat (setq i (sslength ssBlocks))
            (setq block (ssname ssBlocks (setq i (1- i))))
            (setq block_vla (vlax-ename->vla-object block))
            (vla-GetBoundingBox block_vla 'botLeftPt 'topRightPt)
            (setq botLeftPt (vlax-safearray->list botLeftPt)
                  topRightPt (vlax-safearray->list topRightPt)
                  topLeftPt (list (car botLeftPt) (cadr topRightPt) 0)
                  botRightPt (list (car topRightPt) (cadr botLeftPt) 0)
            )
            (setq 
              rightMid (list 
                          (/ (+ (car topRightPt) (car botRightPt)) 2) 
                          (/ (+ (cadr topRightPt) (cadr botRightPt)) 2)
                        )

              leftMid (list 
                          (/ (+ (car topLeftPt) (car botLeftPt)) 2) 
                          (/ (+ (cadr topLeftPt) (cadr botLeftPt)) 2)
                      )
              
              topMid (list 
                          (/ (+ (car topLeftPt) (car topRightPt)) 2) 
                          (/ (+ (cadr topLeftPt) (cadr topRightPt)) 2)
                      )

              botMid (list 
                          (/ (+ (car botLeftPt) (car botRightPt)) 2) 
                          (/ (+ (cadr botLeftPt) (cadr botRightPt)) 2)
                      )
            )
            (setq midPoints (list rightMid leftMid topMid botMid))
            (setq count 0
                  landingPt (list NIL NIL))
            (while (and (/= (car landingPt) NIL) (/= (cadr landingPt) NIL))
                (setq point (nth count midPoints))
                (setq landingPt (getLandingPoint point LeaderLineLen))
                (setq count (1+ count))
            )
            (princ (list point landingPt))
        )
    )
)

(defun getLandingPoint(leaderPt leadLineLen / angle landPt xi yi xf yf)
    (setq angle (deg2Rad 15)
          landPt (list NIL NIL)
    )
    (while (and (<= angle (deg2Rad 45)) (not (isPointInCollision landPt)))
        (setq xi (car leaderPt)
              yi (cadr leaderPt)
              xf (+ (* (cos angle) leadLineLen) xi)
              yf (+ (* (sin angle) leadLineLen) yi)
              landPt (list xf yf)
              angle (+ (deg2Rad 5) angle)
        )
    )
    landPt
)

(defun isPointInCollision(point / ssObjects isCollide i objEname objVla botLeftPt topRightPt)
  (setq ssObjects (ssget "A"))
  (setq isCollide NIL)
  (if (> (sslength ssObjects) 0)
    (repeat (setq i (sslength ssObjects))
      (setq objEname (ssname ssObjects (setq i (1- i))))
      (setq objVla (vlax-ename->vla-object objEname))
      (vla-GetBoundingBox objVla 'botLeftPt 'topRightPt)
      (if 
          (and 
            (<= (car botLeftPt) (car point))
            (<= (car point) (car topRightPt))
            (<= (cadr botLeftPt) (cadr point))
            (<= (cadr point) (cadr topRightPt))
          )
          (setq isCollide T)
      )
    )
  )
  isCollide
)

(defun deg2Rad (deg)
  (* pi (/ deg 180.0))
)
