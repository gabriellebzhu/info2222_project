<center>
<div class="column-container">
    <div class="left-column" id="posts-filter">

        <form action="/action_page.php">
            % if len(classes) == 0:
                <p>You currently have not joined any classes. There are no resources to view.</p>
            % else:
                <div class="filter-entry" id="filter-class">
                    <p>Select a class:</p>
                    % for i in range(0, len(classes)):
                        <input type="checkbox" id="class{{i}}" name="class{{i}}" value="{{!classes[i]}}">
                        <label for="class{{i}}">Include {{!classes[i]}}</label><br>
                    % end
                </div>

                <div class="filter-entry" id="filter-author">
                    <p>Select the types of author (Staff or Student)</p>
                    <input type="checkbox" id="filter-staff" name="filter-staff" value="1">
                    <label for="filter-staff">Staff</label><br>
                    <input type="checkbox" id="filter-student" name="filter-student" value="1">
                    <label for="filter-student">Student</label><br>
                </div>

                <input type="hidden" name="post-type" value="post-filter"/>
                <input type="submit" value="Submit">

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

        <div class="entry">
            <p><a href="/posts/new">Create a post</a></p>
        </div>
    </div>

</div>
</center>
