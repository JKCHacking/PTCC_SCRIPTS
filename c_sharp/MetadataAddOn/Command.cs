using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Collections.Generic;

namespace MetadataAddOn
{
    [Transaction(TransactionMode.Manual)]
    public class Command : IExternalCommand
    {
        public Result Execute(
            ExternalCommandData commandData,
            ref string message,
            ElementSet elements)
        {
            UIApplication uiapp = commandData.Application;
            UIDocument uidoc = uiapp.ActiveUIDocument;
            Document doc = uidoc.Document;
            Application app = uiapp.Application;

            // get all the family elements
            FilteredElementCollector elColl = new FilteredElementCollector(doc);
            IList<Element> families = elColl.OfClass(typeof(Family)).ToElements();

            // get the json data and convert to dictionary
            string jsonFileParam = OpenFile("json");
            if (jsonFileParam != "")
            {
                MetadataAttacher attacher = new MetadataAttacher(app, jsonFileParam);
                attacher.AddMetadata(doc, families);
                return Result.Succeeded;
            } 
            else
            {
                app.WriteJournalComment("[DEBUG] Cannot open json file.", true);
                return Result.Failed;
            }          
        }
        private string OpenFile(string ext)
        {
            string fileParam = "";
            string filter = string.Format("{0} File (*.{1})|*.{1}", ext.ToUpper(), ext);
            FileOpenDialog fileDialog = new FileOpenDialog(filter);
            ItemSelectionDialogResult res = fileDialog.Show();
            if (res == ItemSelectionDialogResult.Confirmed)
            {
                ModelPath modelPath = fileDialog.GetSelectedModelPath();
                fileParam = ModelPathUtils.ConvertModelPathToUserVisiblePath(modelPath);
            }
            return fileParam;
        }
    }

    
}
