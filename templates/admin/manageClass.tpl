<div class="column-container">
    <div class="left-column" id="class-list-section">
        % if len(classes) == 0:
          <p>You currently are not managing any classes</p>
        % else:
          <p>Select a class to manage:</p>
        
        % end

        <ul class="left-column-list" >
            % for i in range(0, len(classes)):
              <li>
                <a href="/manage/{{classes[i]}}">{{classes[i]}}</a>
              </li>
            % end
        </ul>
    </div>

    <div class="right-column" id="mute-ban-section">
        <div class="entry">
            <p>Mute students in {{!class_code}}. They will no longer be able to post. This action cannot be undone.</p>
            <form name="mute-student" action="/manage/{{!class_code}}" method="post">
                <select class="select-students" name="mute-students" id="mute-students" multiple>
                    % for student in [elem for elem in students if elem not in muted]:
                    <option value="{{!student}}">{{!student}}</option>
                    % end
                </select>

                <input type="hidden" name="manage-type" value="mute-student"/>
                <button type="submit">Mute</button>
            </form>
        </div>

        <div class="entry">
            <p>Unmute a student in {{!class_code}}.</p>
            <form name="unmute-student" action="/manage/{{!class_code}}" method="post">
                <select class="select-students" name="unmute-students" id="unmute-students" multiple>
                    % for student in muted:
                    <option value="{{!student}}">{{!student}}</option>
                    % end
                </select>
                <input type="hidden" name="manage-type" value="unmute-student"/>
                <button type="submit">Unmute</button>
            </form>
        </div>

        <div class="entry">
            <p>Ban a student from {{!class_code}}. They will be removed from the course and will not be able to rejoin.</p>
            <form name="ban-student" action="/manage/{{!class_code}}" method="post">
                <select class="select-students" name="ban-students" id="ban-students" multiple>
                    % for student in [elem for elem in students if elem not in banned]:
                    <option value="{{!student}}">{{!student}}</option>
                    % end
                </select>
                <input type="hidden" name="manage-type" value="ban-student"/>
                <button type="submit">Ban</button>
            </form>
        </div>

        <div class="entry">
            <p>Unban a student from {{!class_code}}.</p>
            <form name="unban-student" action="/manage/{{!class_code}}" method="post">
                <select class="select-students" name="unban-students" id="unban-students" multiple>
                    % for student in banned:
                    <option value="{{!student}}">{{!student}}</option>
                    % end
                </select>
                <input type="hidden" name="manage-type" value="unban-student"/>
                <button type="submit">Unban</button>
            </form>
        </div>
    </div>
</div>