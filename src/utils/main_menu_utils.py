

def open(self):
        self.raw_img_dir = tk.filedialog.askopenfilename(initialdir="/", 
                                                title="Select file",
                                                filetypes = [("Raw Hyperspectral Image", "*.raw"),
                                                             ("Numpy Array", "*.npy")
                                                             ])
        
        # this makes sure that if the user selected an image and then
        # tried to open another image but cancelled the process the previous image is still displayed.
        if not self.raw_img_dir:  # Check if raw_img_dir is empty
            # Read the path from the img_dir_record.txt file
            with open(history_path, 'r') as f:
                raw_img_dir = f.read().strip()
                self.raw_img_dir = raw_img_dir
                
        
        # Save the raw_img_dir to a text file in the history folder
        os.makedirs('history', exist_ok=True) #make sure the history folder exists. if not creates one.
        with open(history_path, 'w') as f:
            f.write(self.raw_img_dir)
            
        ######################### RECENT FILES #################
        # first reads all the existing paths from the file into a list. 
        # It then checks if the current path already exists in the list. 
        # If it doesn’t, the path is added to the top of the list. 
        # Finally, all the paths are written back to the file. 
        # This ensures that the most recent path is always at the top and there are no duplicates.
        
        # Read the existing paths
        with open(recent_file_path, 'r') as f:
            lines = f.read().splitlines()

        # If the path already exists in the file, remove it
        if self.raw_img_dir in lines:
            lines.remove(self.raw_img_dir)

        # Add the path to the top of the list
        lines.insert(0, self.raw_img_dir)

        # Only keep the 5 most recent paths
        lines = lines[:5]
        
        # Write the paths back to the file
        with open(recent_file_path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
                
        
        self.Dataloaded = False
        #using multithreading to show the loading dialog box while data is loading
        threading.Thread(target = self.loadData).start()
        
        self.dataLoadingScreen()
        print("********************1") 