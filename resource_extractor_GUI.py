import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from bw_read_xml import BattWarsLevel
import xml.etree.ElementTree as etree
import json
import os
import shutil
from pathlib import Path

class BattWarsExtractor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Battalion Wars Reousrce Extractor")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.xml_frame = ttk.Frame(self.notebook)
        self.resource_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.xml_frame, text="XML Extractor")
        self.notebook.add(self.resource_frame, text="Resource Extractor")

        self.setup_xml_tab()
        self.setup_resource_tab()
    
    def setup_xml_tab(self):
        # Input file entry with Browse button
        tk.Label(self.xml_frame, text="Input XML File:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_input = tk.Entry(self.xml_frame, width=50)
        self.entry_input.grid(row=0, column=1, padx=5, pady=5)
        browse_button = tk.Button(self.xml_frame, text="Browse", command=self.browse_xml_file)
        browse_button.grid(row=0, column=2, padx=5, pady=5)

        # ID entry
        tk.Label(self.xml_frame, text="Unit ID:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_id = tk.Entry(self.xml_frame, width=50)
        self.entry_id.grid(row=1, column=1, padx=10, pady=5)

        # Checkboxes frame
        checkbox_frame = ttk.LabelFrame(self.xml_frame, text="Options")
        checkbox_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Passengers checkbox
        self.var_passengers = tk.IntVar(value=1)
        chk_passengers = tk.Checkbutton(checkbox_frame, text="Include Passengers", variable=self.var_passengers)
        chk_passengers.pack(side=tk.LEFT, padx=10, pady=5)

        # mpscript checkbox
        self.var_mpscript = tk.IntVar(value=1)
        chk_mpscript = tk.Checkbutton(checkbox_frame, text="Include mpscript", variable=self.var_mpscript)
        chk_mpscript.pack(side=tk.LEFT, padx=10, pady=5)

        # Process button
        self.process_xml_button = tk.Button(self.xml_frame, text="Process XML", command=self.process_xml_file)
        self.process_xml_button.grid(row=3, column=0, columnspan=3, pady=10)

    def setup_resource_tab(self):
        # Source directory
        tk.Label(self.resource_frame, text="Source Directory:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_src = tk.Entry(self.resource_frame, width=50)
        self.entry_src.grid(row=0, column=1, padx=10, pady=5)
        browse_src_button = tk.Button(self.resource_frame, text="Browse", command=self.browse_src_dir)
        browse_src_button.grid(row=0, column=2, padx=5, pady=5)

        # Destination directory
        tk.Label(self.resource_frame, text="Destination Directory:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_dst = tk.Entry(self.resource_frame, width=50)
        self.entry_dst.grid(row=1, column=1, padx=10, pady=5)
        browse_dst_button = tk.Button(self.resource_frame, text="Browse", command=self.browse_dst_dir)
        browse_dst_button.grid(row=1, column=2, padx=5, pady=5)

        # JSON file
        tk.Label(self.resource_frame, text="Resource JSON:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_json = tk.Entry(self.resource_frame, width=50)
        self.entry_json.grid(row=2, column=1, padx=10, pady=5)
        browse_json_button = tk.Button(self.resource_frame, text="Browse", command=self.browse_json_file)
        browse_json_button.grid(row=2, column=2, padx=5, pady=5)

        # Process button
        self.process_resource_button = tk.Button(self.resource_frame, text="Extract Resources",
                                               command=self.process_resources)
        self.process_resource_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.resource_frame, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

    def browse_xml_file(self):
        filename = filedialog.askopenfilename(
            title="Select XML File",
            filetypes=(("XML Files", "*.xml"), ("All Files", "*.*"))
        )
        if filename:
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, filename)

    def browse_src_dir(self):
        dirname = filedialog.askdirectory(title="Select Source Directory")
        if dirname:
            self.entry_src.delete(0, tk.END)
            self.entry_src.insert(0, dirname)

    def browse_dst_dir(self):
        dirname = filedialog.askdirectory(title="Select Destination Directory")
        if dirname:
            self.entry_dst.delete(0, tk.END)
            self.entry_dst.insert(0, dirname)

    def browse_json_file(self):
        filename = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )
        if filename:
            self.entry_json.delete(0, tk.END)
            self.entry_json.insert(0, filename)

    def process_xml_file(self):
        # Process the XML file and create output files
        unit_id = self.entry_id.get()
        passenger_control = self.var_passengers.get()
        mpscript_control = self.var_mpscript.get()
        input_file = self.entry_input.get()

        if not unit_id or not input_file:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            with open(input_file, "r") as f:
                bwlevel = BattWarsLevel(f)

            root = bwlevel.obj_map[unit_id]
            copied = {unit_id: True}
            out = []
            resources = {}

            def traverse_recursively(bwobj):
                copied[bwobj.id] = True

                # Modify only the text within mPassenger items if "Include Passengers" is unchecked
                if passenger_control == 0:
                    m_passenger_pointer = bwobj._xml_node.find(".//Pointer[@name='mPassenger']")
                    if m_passenger_pointer is not None:
                        for item in m_passenger_pointer.findall("Item"):
                            item.text = "0"  # Set each existing <Item> in mPassenger to "0"

                # Modify only the text within mpScript items if "Include mpScript" is unchecked
                if mpscript_control == 0:
                    mp_script_resource = bwobj._xml_node.find(".//Resource[@name='mpScript']")
                    if mp_script_resource is not None:
                        for item in mp_script_resource.findall("Item"):
                            item.text = "0"  # Set each existing <Item> in mpScript to "0"

                out.append(bwobj._xml_node)

                for attrname, attrdata in bwobj.attributes.items():
                    if attrdata.tag == "Pointer":
                        for sub in attrdata:
                            id = sub.text
                            if id != "0" and id not in copied:
                                traverse_recursively(bwlevel.obj_map[id])
                    elif attrdata.tag == "Resource":
                        for sub in attrdata:
                            resource_id = sub.text
                            if resource_id != "0" and resource_id not in copied:
                                copied[resource_id] = True
                                resource = bwlevel.obj_map[resource_id]
                                out.append(resource._xml_node)
                                if resource.type not in resources:
                                    resources[resource.type] = []
                                resources[resource.type].append(resource.get_attr_value("mName"))

            traverse_recursively(root)

            # Save XML and JSON
            outxml = "out.xml"
            outtxt = "resources.json"
            out.sort(key=lambda x: x.get("type"))
            xmlroot = etree.Element("Instances")
            for val in out:
                xmlroot.append(val)

            tree = etree.ElementTree(xmlroot)
            with open(outxml, "wb") as f:
                tree.write(f)

            with open(outtxt, "w") as f:
                json.dump(resources, f, indent=4)

            messagebox.showinfo("Success",
                              f"Processed file saved as {outxml} and resources as {outtxt}\n\n"
                              f"Would you like to extract the resources now?")

            # Switch to resource tab and load the JSON file
            self.notebook.select(1)
            self.entry_json.delete(0, tk.END)
            self.entry_json.insert(0, outtxt)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def process_resources(self):
        # Process and extract resource files
        src = self.entry_src.get()
        dst = self.entry_dst.get()
        json_file = self.entry_json.get()

        if not all([src, dst, json_file]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            src = os.path.abspath(src)
            src_prefix = len(src) + len(os.path.sep)

            # Load JSON data
            with open(json_file, "r") as f:
                data = json.load(f)

            total_items = sum(len(items) for items in data.values())
            processed_items = 0

            # Traverse JSON data
            for key, items in data.items():
                for item in items:
                    if key == "cNodeHierarchyResource":
                        # Copy folder and all files if one file matches within cNodeHierarchyResource
                        folder_copied = False
                        for root, _, files in os.walk(src):
                            for filename in files:
                                file_path = os.path.join(root, filename)
                                file_name_extracted = Path(file_path).stem

                                if item == file_name_extracted:
                                    relative_dir = root[src_prefix:]
                                    target_dir = os.path.join(dst, relative_dir)

                                    # Create target directory and copy all files in this folder
                                    os.makedirs(target_dir, exist_ok=True)
                                    for related_file in files:
                                        original = os.path.join(root, related_file)
                                        target = os.path.join(target_dir, related_file)

                                        try:
                                            shutil.copy2(original, target)
                                        except Exception as e:
                                            print(f"Error copying {related_file}: {e}")

                                    folder_copied = True
                                    break
                            if folder_copied:
                                break
                    else:
                        # Copy only the specific referenced file for other keys
                        for root, _, files in os.walk(src):
                            for filename in files:
                                file_path = os.path.join(root, filename)
                                file_name_extracted = Path(file_path).stem

                                if item == file_name_extracted:
                                    relative_dir = root[src_prefix:]
                                    target_dir = os.path.join(dst, relative_dir)
                                    os.makedirs(target_dir, exist_ok=True)

                                    original = os.path.join(root, filename)
                                    target = os.path.join(target_dir, filename)

                                    try:
                                        shutil.copy2(original, target)
                                    except Exception as e:
                                        print(f"Error copying {filename}: {e}")
                                    break

                    processed_items += 1
                    self.progress["value"] = (processed_items / total_items) * 100
                    self.update_idletasks()

            messagebox.showinfo("Success", "Resource extraction completed successfully!")
            self.progress["value"] = 0

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.progress["value"] = 0

if __name__ == "__main__":
    app = BattWarsExtractor()
    app.mainloop()

