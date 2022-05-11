<center>

<div class="column-container">
    <div class="left-column" id="posts-filter">
        % if len(classes) == 0:
          <p>You currently have not joined any classes</p>
        % else:
          <p>Select a class:</p>
        
        % end

        <ul class="left-column-list" >
            % for i in range(0, len(classes)):
              <li>
                <a href="/manage/{{classes[i]}}">{{classes[i]}}</a>
              </li>
            % end
        </ul>
    </div>




    <div class="right-column" id="class-manager-section">
        % if msg:
        <div class="entry">
          <p>{{!msg}}</p>
        </div>
        % end

        <div class="entry">
            <p>Create a class. Enter the class code and the class name.</p>
            <form name="add-class" action="/manage" method="post">
              <input name="class-code-input" autocomplete="off">
              <input name="class-name-input" autocomplete="off">
              <input type="hidden" name="manage-type" value="add-class"/>
              <button type="submit">Create</button>
            </form>
          </div>
      
          <div class="entry">
            <p>Remove a class and archive all posts. Enter the class code.</p>
            <form name="add-class" action="/manage" method="post">
                <input name="class-info-input" autocomplete="off">
                <input type="hidden" name="manage-type" value="del-class"/>
                <button type="submit">Delete</button>
            </form>
          </div>
    </div>

</div>
</center>
