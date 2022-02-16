Sub fitGraphics()
   Dim oDoc As Object
   Dim oSheet As Object
   Dim aCell As Object
   Dim g as Object
   Dim c As Integer
   Dim s As new com.sun.star.awt.Size
   Dim gp As new com.sun.star.awt.Point
   Dim ap As new com.sun.star.awt.Point
   Dim p As new com.sun.star.awt.Point
   Dim xAdjust As Long
   Dim yAdjust As Long
   Dim rowHeight As Long
   Dim colWidth As Long

   oDoc = ThisComponent
   oSheet = oDoc.CurrentController.ActiveSheet
   c = oSheet.DrawPage.count

   Do While c >= 1
         g = oSheet.DrawPage(c - 1)
         if InStr(g.ShapeType,"GraphicObjectShape") > 0 then
            s = g.getSize()
            aCell = g.anchor
            s.Height = oSheet.Rows(aCell.CellAddress.Row).Height
            s.Width = oSheet.Columns(aCell.CellAddress.Column).Width
            g.setSize(s)
         endif
         c = c - 1
   Loop
End Sub