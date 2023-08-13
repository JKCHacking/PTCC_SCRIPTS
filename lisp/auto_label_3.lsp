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
  (command "mspace\n")
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