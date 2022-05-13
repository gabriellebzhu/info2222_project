<center>
    <div id="return-button">
    </div>

    <div class="post-view-section">
        <div class="post-view-entry">
            <p>Post #{{!post_id}}</p>
        </div>

        <div id="post-view-title">
            <p>{{!title}}</p>
            <div>
                <p>{{!likes}}</p>
                <button>Like</button>
            </div>
        </div>

        <div class="post-view-entry" id="post-view-tags">
            <div class="tag tag-view-class" id="post-view-class">
                <p>{{!post_class}}</p>
            </div>
            
            <!-- <div> -->
                % for i in range(0, len(tags)):
                <div class="tag tag-view" id="post-view-tag{i}">
                    <p>{{!tags[i]}}</p>
                </div>
                % end
            <!-- </div> -->
        </div>

        <div class="post-view-entry" id="post-view-meta">
            <p>Posted by <a href="#top">{{username}}</a></p>
            <p>Posted at {{!date}}</p>
        </div>

        <div class="post-view-entry" id="post-view-attachments">
            % for i in range(0, len(file_paths)):
                <a href="{{!file_paths[i]}}">{{!file_names[i]}}</a>
            % end
        </div>

        <div class="post-view-entry" id="post-view-body">
            <p>
                {{body}}
            </p>
        </div>

    </div>

</center>

<script>
    returnBtn = document.getElementById("return-button");
    prev = window.sessionStorage.getItem("temp");
    if (prev === "search") {
        <a class="button" href="javascript:history.back()">Back to Filter</a>
    } else {
        <a class="button" href="/posts">Back to Posts</a>
    }
    window.sessionStorage.deleteItem("temp");
</script>