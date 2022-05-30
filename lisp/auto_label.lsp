(vl-load-com)

(defun PTCC:AutoBlockLabel( / leaderLineLen
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
                           botLeftPt topRightPt topLeftPt botRightPt
                           midPts
                           leaderPt
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
                          0
                        )

              leftMid (list 
                          (/ (+ (car topLeftPt) (car botLeftPt)) 2) 
                          (/ (+ (cadr topLeftPt) (cadr botLeftPt)) 2)
                          0
                      )
              
              topMid (list 
                          (/ (+ (car topLeftPt) (car topRightPt)) 2) 
                          (/ (+ (cadr topLeftPt) (cadr topRightPt)) 2)
                          0
                      )

              botMid (list 
                          (/ (+ (car botLeftPt) (car botRightPt)) 2) 
                          (/ (+ (cadr botLeftPt) (cadr botRightPt)) 2)
                          0
                      )
            )
            (setq midPts (list rightMid leftMid topMid botMid)
                  angRanges (list (list 15 45)
                             (list 135 180)
                             (list 15 45)
                             (list 285 325)
                        )
            )
            (setq count 0
                  landingPt (list NIL NIL))
            (while (and (= (car landingPt) NIL)
                        (= (cadr landingPt) NIL)
                        (<= count (1- (length midPts))))
                (setq leaderPt (nth count midPts))
                (setq angRange (nth count angRanges))
                (setq landingPt (getLandingPoint leaderPt
                                                 angRange
                                                 leaderLineLen))
                (setq count (1+ count))
            )
            ;for the case when theres really no optimal space to put the
            ;landing point then just use the first choice.
            ;and let the user fix manually.
            (cond 
              ((and 
                 (= count (1- (length midPts)))
                 (= (car landingPt) NIL)
                 (= (cadr landingPt) NIL)
                )
                (setq landingPt (computeLandPoint (nth 0 midPts)
                                                  (nth 0 angRanges)
                                                  leaderLineLen)
                )
              )
            )
            (setq mleaderTxt (vla-get-Name block_vla))
            (addMLeader modelSpace leaderPt landingPt mleaderTxt)
        )
    )
)

(defun addMLeader (modelSpace leaderPt landingPt text / mleaderObj
                                                        points
                                                        pointList)
  (setq points (vlax-make-safearray vlax-vbDouble '(0 . 5)))
  (setq pointList (append leaderPt landingPt))
  (vlax-safearray-fill points pointList)
  (setq mleaderObj (vla-AddMLeader modelSpace points 0))
  (vla-put-TextString mleaderObj text)
)

(defun computeLandPoint (leaderPt ang leadLineLen / landPt xi yi xf yf)
  (setq xi (car leaderPt)
        yi (cadr leaderPt)
        xf (+ (* (cos s_ang) leadLineLen) xi)
        yf (+ (* (sin s_ang) leadLineLen) yi)
        landPt (list xf yf 0)
  )
  landPt  
)

(defun getLandingPoint(leaderPt angRange leadLineLen / s_ang e_ang inc_ang
                                                       landPt)
    (setq s_ang (deg2Rad (car angRange))
          e_ang (deg2Rad (cadr angRange))
          inc_ang (deg2Rad 5)
          landPt (list NIL NIL)
    )
    (while 
      (and 
        (<= s_ang e_ang)
        (or
          (isPointInCollision landPt)
          (= (car landPt) NIL)
          (= (cadr landPt) NIL)
        )
      )
      (setq landPt (computeLandPoint leaderPt s_ang leadLineLen)
            s_ang (+ s_ang inc_ang)
      )
    )
    (if (isPointInCollision landPt)
      (setq landPt (list NIL NIL))
    )
    landPt
)

(defun isPointInCollision(point / 
                          ssObjects
                          isCollide
                          i
                          objEname
                          objVla
                          botLeftPt
                          topRightPt)
  (setq ssObjects (ssget "A"))
  (setq isCollide NIL)
  (if (> (sslength ssObjects) 0)
    (repeat (setq i (sslength ssObjects))
      (setq objEname (ssname ssObjects (setq i (1- i))))
      (setq objVla (vlax-ename->vla-object objEname))
      (vla-GetBoundingBox objVla 'botLeftPt 'topRightPt)
      (setq botLeftPt (vlax-safearray->list botLeftPt)
            topRightPt (vlax-safearray->list topRightPt)
      )
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
