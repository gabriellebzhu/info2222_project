
<div class="column-container" id="chatbox">
  <div class="left-column" id="user-column">
    <p>
      Welcome back, {{username}}! {{err_msg}}
      <br>
      Select a friend to chat with:
    </p>

    <ul class="left-column-list" id="friend-list">
      % for i in range(0, len(friend_usernames)):
        <li>
          <a href="/chat/{{friend_ids[i]}}">{{friend_usernames[i]}}</a>
        </li>
      % end
    </ul>
  </div>

  <div class="right-column" id="add-friend-column">
    <h2>Add Friends</h2>

    % if add_msg:
    <div class="entry">
      <p>{{!add_msg}}</p>
    </div>
    % end
  
    <div class="entry">
      <p>Add a friend by their username</p>
      <form name="add-id-friend" action="/friends" method="post">
        <input name="username-input" autocomplete="off">
        <input type="hidden" name="add-type" value="add-username"/>
        <button type="submit">Add</button>
      </form>
    </div>

    <div class="entry">
      <p>Find a random friend from one of your classes</p>
      <form name="add-class-friend" action="/friends" method="post">
        <input type="hidden" name="add-type" value="add-class"/>
        <button type="submit">Find</button>
      </form>
    </div>
  </div>
</div>
