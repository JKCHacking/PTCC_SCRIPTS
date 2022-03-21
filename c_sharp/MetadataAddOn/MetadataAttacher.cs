using Autodesk.Revit.DB;
using Autodesk.Revit.ApplicationServices;
using System.IO;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace MetadataAddOn
{
    internal class MetadataAttacher
    {
        string jsonMetdataPath;
        Application app;

        public MetadataAttacher(Application app, string jsonMetdataPath)
        {
            this.app = app;
            this.jsonMetdataPath = jsonMetdataPath;
        }
        public void AddMetadata(Document doc, IList<Element> families)
        {
            string paramJson = File.ReadAllText(jsonMetdataPath);
            Dictionary<string, Dictionary<string, string>> paramDict = JsonConvert.
                DeserializeObject<Dictionary<string, Dictionary<string, string>>>(paramJson);

            ForgeTypeId paramGroup = GroupTypeId.Data;
            ForgeTypeId paramType = SpecTypeId.String.Text;
            foreach (Family fam in families)
            {
                if (fam.IsEditable && paramDict.ContainsKey(fam.Name))
                {
                    string famName = fam.Name;
                    // get the family document object from the family object
                    Document famDoc = doc.EditFamily(fam);
                    using (Transaction t_famdoc = new Transaction(famDoc))
                    {
                        // ============================ADDING KEYS TO PARAMETERS=====================================
                        t_famdoc.Start("Adding metadata keys");
                        // add the general parameters
                        IDictionary<string, string> genParams = paramDict["general"];
                        foreach (var kvp in genParams)
                        {
                            // add parameter
                            famDoc.FamilyManager.AddParameter(kvp.Key, paramGroup, paramType, false);
                        }
                        // add the specific parameters
                        try
                        {
                            IDictionary<string, string> specParams = paramDict[famName];
                            foreach (var kvp in specParams)
                            {
                                // add parameter
                                famDoc.FamilyManager.AddParameter(kvp.Key, paramGroup, paramType, false);
                            }
                        }
                        catch (KeyNotFoundException)
                        {
                            app.WriteJournalComment(string.Format("[DEBUG] Cannot find {0}", famName), true);
                        }
                        t_famdoc.Commit();

                        // ============================ADDING VALUES TO PARAMETERS=====================================
                        t_famdoc.Start("Adding metadata values");
                        // add the general parameters
                        foreach (var kvp in genParams)
                        {
                            // retrieve the family parameter
                            FamilyParameter fParam = famDoc.FamilyManager.get_Parameter(kvp.Key);
                            // assign value of parameter
                            famDoc.FamilyManager.Set(fParam, kvp.Value);
                        }
                        // add the specific parameters
                        try
                        {
                            IDictionary<string, string> specParams = paramDict[famName];
                            foreach (var kvp in specParams)
                            {
                                // retrieve the family parameter
                                FamilyParameter fParam = famDoc.FamilyManager.get_Parameter(kvp.Key);
                                // assign value of parameter
                                famDoc.FamilyManager.Set(fParam, kvp.Value);
                            }
                        }
                        catch (KeyNotFoundException)
                        {
                            app.WriteJournalComment(string.Format("[DEBUG] Cannot find {0}", famName), true);
                        }
                        t_famdoc.Commit();
                    }

                    string path = Path.GetTempPath();
                    string name = fam.Name;
                    string fname = name + ".rfa";
                    string fpath = path + fname;
                    famDoc.SaveAs(fpath);
                    famDoc.LoadFamily(doc, new FamilyOptions());
                }
            }
        }
    }
}
