<center>
<div class="column-container">
    <div class="left-column" id="posts-filter">

        <form action="/posts/show" method="post">
            <h3>Filter Posts</h3>
            % if len(classes) == 0:
                <p>You currently have not joined any classes. There are no resources to view.</p>
            % else:
                <button type="button" class="accordion">Filter by Class</button>
                <div class="filter-entry panel" id="filter-class">
                    <p class="tooltip">Select classes to show:</p>
                    % for i in range(0, len(classes)):
                        <div class="select">
                            <input type="checkbox" id="class{{i}}" name="class-choice" value="{{!classes[i]}}" checked>
                            <label for="class{{i}}">{{!classes[i]}}</label><br>
                        </div>
                    % end
                </div>

                <button type="button" class="accordion">Filter by Author</button>
                <div class="filter-entry panel" id="filter-class">
                    <div class="select">
                        <input type="checkbox" id="filter-staff" name="filter-choice" value="1">
                        <label for="filter-staff">Staff</label><br>
                    </div>

                    <div class="select">
                        <input type="checkbox" id="filter-student" name="filter-choice" value="0">
                        <label for="filter-student">Student</label><br>
                    </div>
                </div>

                <button type="button" class="accordion">Filter by Tag</button>
                <div class="filter-entry panel" id="filter-class">
                    % for i in range(0, len(tags)):
                        <div class="select">
                            <input type="checkbox" id="tags{{i}}" name="tag-choice" value="{{!tags[i]}}">
                            <label for="tags{{i}}">{{!tags[i]}}</label><br>
                        </div>
                    % end
                    <div class="select">
                        <p class="tooltip">Enter other tags separated by spaces</p>
                        <input type="text" id="tag-search" name="tag-search" placeholder="tag1 tag2">
                    </div>
                </div>

                <button type="button" class="accordion">Search (regex)</button>
                <div class="filter-entry panel" id="filter-class">
                    <p class="tooltip">Search all fields with regex:</p>
                    <div class="search">
                        <input type="text" id="search" name="search" placeholder="Regular Expression">
                    </div>
                </div>


                <input type="hidden" name="post-type" value="post-filter"/>
                <div id="filter-submit">
                <input type="submit" value="Submit">
                </div>

            % end
        </form>
    </div>




    <div class="right-column" id="class-join-section">
        % if msg:
        <div class="entry">
          <p>{{!msg}}</p>
        </div>
        % end

        <div class="entry">
            <p>Join a class. Enter the class code or the class name.</p>
            <form name="join-class" action="/posts" method="post">
              <input name="class-info-input" autocomplete="off">
              <input type="hidden" name="post-type" value="join-class"/>
              <button type="submit">Join</button>
            </form>
        </div>

        <div class="entry">
            <p>Leave a class. Enter the class code or the class name</p>
            <form name="leave-class" action="/manage" method="post">
                <input name="class-info-input" autocomplete="off">
                <input type="hidden" name="post-type" value="leave-class"/>
                <button type="submit">Delete</button>
            </form>
        </div>

        <div class="entry" id="create-post-button" onclick="toNew()">
            <h3><a href="/posts/new">Create a post</a></h3>
        </div>
    </div>

</div>
</center>
<script>
    function toNew() {
        document.location.href = "posts/new";
    }

    var acc = document.getElementsByClassName("accordion");
    var i;

    for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function(event) {
        /* Toggle between adding and removing the "active" class,
        to highlight the button that controls the panel */
        this.classList.toggle("active");

        /* Toggle between hiding and showing the active panel */
        var panel = this.nextElementSibling;
        
        if (panel.style.display === "flex") {
        panel.style.display = "none";
        } else {
        panel.style.display = "flex";
        }
        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
        } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
        }
    });
    } 
</script>