<center>
<div class="column-container">
    <div class="left-column" id="posts-filter">

        <form action="/posts/show" method="post">
            % if len(classes) == 0:
                <p>You currently have not joined any classes. There are no resources to view.</p>
            % else:
                <div class="filter-entry" id="filter-class">
                    <p>Select classes to show:</p>
                    % for i in range(0, len(classes)):
                        <div class="select">
                            <input type="checkbox" id="class{{i}}" name="class-choice" value="{{!classes[i]}}">
                            <label for="class{{i}}">{{!classes[i]}}</label><br>
                        </div>
                    % end
                </div>

                <div class="filter-entry" id="filter-author">
                    <p>Select the types of author</p>

                    <div class="select">
                        <input type="checkbox" id="filter-staff" name="filter-choice" value="1">
                        <label for="filter-staff">Staff</label><br>
                    </div>

                    <div class="select">
                        <input type="checkbox" id="filter-student" name="filter-choice" value="0">
                        <label for="filter-student">Student</label><br>
                    </div>
                </div>

                <div class="filter-entry" id="filter-tags">
                    <p>Select tags:</p>
                    % for i in range(0, len(tags)):
                        <div class="select">
                            <input type="checkbox" id="tags{{i}}" name="tag-choice" value="{{!tags[i]}}">
                            <label for="tags{{i}}">{{!tags[i]}}</label><br>
                        </div>
                    % end
                    <div class="select">
                        <input type="text" id="tag-search" name="tag-search" placeholder="Tags (space-separated)">
                    </div>
                </div>

                <div class="filter-entry" id="filter-search">
                    <p>Search all fields with regex:</p>
                    <div class="search">
                        <input type="text" id="search" name="search" placeholder="Regular Expression">
                    </div>
                </div>


                <input type="hidden" name="post-type" value="post-filter"/>
                <input type="submit" value="Submit">

            % end
        </form>
    </div>




    <div class="right-column" id="filtered-section">
        <p>Your query was: <br>
            <span>{{!query}}</span>
        </p>

        % if len(data) == 0:
            <div class="filtered-entry">
                <p>No entries found.</p>
            </div>
        % else:
            % for entry in data:
                <div class="filtered-entry" onclick="toPost('{{!entry[0]}}')">
                    <div id="filtered-title-id">
                        <p class="filtered-id">#{{!entry[0]}}</p>
                        <h3 class="filtered-title">{{!entry[1]}}</h3>
                    </div>
                    <div id="filtered-meta">
                        <p>{{!entry[2]}}</p>
                        <p>{{!entry[3]}}</p>
                    </div>
                    <div class="post-view-entry tag-filtered" id="post-view-tags">
                        <div class="tag tag-view-class" id="post-view-class">
                            <p>{{!entry[4]}}</p>
                         </div>
            
                        % for i in range(0, len(entry[5].split())):
                            <div class="tag tag-view" id="post-view-tag{i}">
                                <p>{{!entry[5].split()[i]}}</p>
                            </div>
                        % end
                    </div>

                    <div class="filtered">
                        % if (len(entry[6]) > 100):
                        {{entry[6][0:100]}} ...
                        % else:
                        {{entry[6]}}
                        % end
                    </div>

                    <div class="filtered">
                        % if (len(entry[7].split()) > 0):
                            Attachments: {{len(entry[7].split())}}
                        % end

                        % if (entry[8] > 0):
                            Likes: {{entry[8]}}
                        % end
                    </div>

                </div>
            % end
        % end
    </div>

</div>
</center>
<script>
    function toPost(id) {
        document.location.href = "posts/" + id;
    }
</script>