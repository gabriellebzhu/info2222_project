% if success == 1:
    <script>
        window.location.replace("/posts/" + "{{!post_id}}")
    </script>
% end

<center>
    <h3 id="new-post-title">Create New Post</h3>
    <div id="post-form-section">
        <form id="post-form" action="/posts/new" method="post" enctype=multipart/form-data>
            <div class="form-line">
                <label for="post-title">Title</label>
                <input id="post-title" type="text" name="post-title">
            </div>

            <div class="form-line">
                <div>
                    <label for="post-class-selector">Class</label>
                    <select name="post-class-selector" id="post-class-selector">
                        % for i in range(0, len(classes)):
                            <option value="{{!classes[i]}}">{{!classes[i]}}</option>
                        % end
                    </select>
                </div>
                <div>
                    <label for="post-tags">Tags</label>
                    <input type="text" name="post-tags" id="post-tags" placeholder="Separate tags with a space.">
                </div>
            </div>

            <div class="form-line"  id="form-body">
                <textarea type="text" class="multi-line-input" name="post-body"
                          placeholder="Your post here. Use html to format."></textarea>
            </div>

            <div class="form-line">
                <input type="file" name="post-attachments" id="post-attachments" multiple="multiple">
            </div>

            <div class="form-line" id="submit-form-line">
                <button type="submit">Post</button>
            </div>

        </form>
    </div>
</center>

<script>
let uploadField = document.getElementById("post-attachments");

uploadField.onchange = function() {
    var msg = "The following files are over the upload limit of 50 MB. Please ensure they are removed.\n\n"
    var totalNumber = 0
    for (var i = 0; i < this.files.length; i++) {
        if (this.files[i].size > 10 * 1048576) {  // 100 MB
            msg += this.files[i].name + "\n"
        } else {
            totalNumber += 1
        };
    }

    if (totalNumber > 30) {  // 100 MB
        msg = "No more than 30 files can be uploaded at once"
        this.value = ""
        alert(msg)
    } else if (totalNumber != this.files.length) {  // 100 MB
        this.value = ""
        alert(msg)
    } 


};
</script>