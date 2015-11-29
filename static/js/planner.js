$(document).ready(function() {

    // Session Storage
    if (!(sessionStorage.viewDate)) {
        var now = new Date();
        sessionStorage.viewDate = now;
    }

    // Use this for debugging to reset localStorage
    //localStorage.clear();

    // Local Storage
    if (!(localStorage.layoutType)) {
        localStorage.layoutType = "Week";
    }

    changeViewLayout(localStorage.layoutType);
});

/*
    Renders the current layoutType to the page

    #TODO Actually make this work with different layouts
*/
function changeViewLayout(viewType) {
    var btns = $(".btn-layout-selector");

    if(localStorage.layoutType == viewType) {
            // Do nothing
    }
    else {
        localStorage.layoutType = viewType;
    }
    
    // Update view based on currently selected layout
    $.ajax({
        url: "/planner/",
        type: "POST",
        dataType: 'html',
        data: 
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            planner_layout: localStorage.layoutType
        },
        success: function(data, textStatus, jqXHR) {
            $('#planner-day-week-month-render-area').empty().append(data);
            changeViewDate("NONE");
        },
    });
}


// Returns the current viewDate stored in sessionStorage
function getViewDate() {
    return new Date(Date.parse(sessionStorage.viewDate));
}

// Sets the sessionStorage viewDate to the specified date (limited to year, month, day)
function setViewDate(year, month, day) {
    sessionStorage.viewDate = new Date(year, month, day);
}

// Changes the date to the specified date & updates necessary fields
function selectDate(year, month, day) {
    setViewDate(year, month, day);
    changeViewDate("NONE");
}

/*
    Changes the current viewDate in sessionStorage based on input:

    @param size
        The size of the change: DAY, WEEK, MONTH, YEAR
    @param amount
        The amount of the change: -1, or 1, preferrably. (1 week, 1 month, -1 week, etc.)

    Prompts all date fields to update to the new viewDate
    Prompts the mini calendar to re-write itself if it's displayed.
*/
function changeViewDate(size, amount) {
    var viewDate = getViewDate();

    if(size === "DAY") {
        viewDate.setDate(viewDate.getDate() + amount);
    }
    else if(size === "WEEK") {
        viewDate.setDate(viewDate.getDate() + 7 * amount);
    }
    else if(size === "MONTH") {
        // When a user changes month, always take them to the 1st of that month.
        viewDate.setDate(1);
        viewDate.setMonth(viewDate.getMonth() + amount);
    }
    else if(size === "YEAR") {
        viewDate.setFullYear(viewDate.getFullYear() + amount);
    }
    else if(size === "TODAY") {
        var now = new Date();
        viewDate = now;
    }
    else if(size === "NONE") {
        // Do nothing, running first time setup or updating the page without changing the view date.
    }
    else {
        throw "changeViewDate() unknown parameter: \"" + size + "\" -- If no change desired, use \"NONE\"";
    }

    sessionStorage.viewDate = viewDate;
    var start_date, end_date;

    switch(localStorage.layoutType) {
        case "Day":
            /*$.ajax({
                url: "/load-day-events/",
                type: "POST",
                dataType: 'html',
                data: 
                {
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    view_start_date: start_date,
                    view_end_date: end_date
                },
                success: function(data, textStatus, jqXHR) {
                    $('#events-in-week-view').empty().append(data);
                },
            });
            try{
                var cal = new miniCal();
                cal.handleDateChange();
            } catch(err) {
                throw "The miniCalendar had an update attempted on it, but it doesn't exist."
            }*/
            document.getElementById("planner-date-month-selector").innerHTML = month_names[viewDate.getMonth()];
            // #TODO: Show the current date as MM/DD formate (11/27)
            break;
        case "Week":
            start_date = getDateOfDay(0);
            end_date   = getDateOfDay(6);

            $.ajax({
                url: "/load-week-events/",
                type: "POST",
                dataType: 'html',
                data: 
                {
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    view_start_date: start_date,
                    view_end_date: end_date
                },
                success: function(data, textStatus, jqXHR) {
                    loadEventUpdateModal();
                    loadCategoryUpdateModal();
                    $('#events-in-week-view').empty().append(data);
                    loadCategoryCreationModal()
                    loadEventCreationModal();
                    loadImportantAndUpcoming();
                },
            });
            try{
                var cal = new miniCal();
                cal.handleDateChange();
            } catch(err) {
                throw "The miniCalendar had an update attempted on it, but it doesn't exist."
            }
            document.getElementById("planner-date-week-selector").innerHTML = getWeekString();
            document.getElementById("planner-date-month-selector").innerHTML = month_names[viewDate.getMonth()];
            break;
        case "Month":
            var temp = getCalFirstDay(),
                start_date = getFullDateString(temp);

            $.ajax({
                url: "/load-month-events/",
                type: "POST",
                dataType: 'html',
                data: 
                {
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    view_start_date: start_date
                },
                success: function(data, textStatus, jqXHR) {
                    $('#events-in-month-view').empty().append(data);
                },
            });

            // Put the long month name in this view
            document.getElementById("planner-date-month-selector").innerHTML = month_names_long[viewDate.getMonth()];
            break;
        default:
            throw "Invalid layout type in changeViewDate(), please use a valid layout type.";
    }
    
    // Update all fields in case they changed
    document.getElementById("planner-date-year-selector").innerHTML = viewDate.getFullYear();
}

function loadCategoryCreationModal() {
    $.ajax({
        url: "/load-category-creation-modal/",
        type: "GET",
        dataType: 'html',
        data:
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data, textStatus, jqXHR) {
            $('#inject-category-creation-modal').empty().append(data);
        },
    });
}

function loadCategoryUpdateModal() {
    $.ajax({
        url: "/load-category-update-modal/",
        type: "GET",
        dataType: 'html',
        data:
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data, textStatus, jqXHR) {
            $('#inject-category-update-modal').empty().append(data);
        },
    });
}

function loadEventCreationModal() {
    $.ajax({
        url: "/load-event-creation-modal/",
        type: "GET",
        dataType: 'html',
        data:
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data, textStatus, jqXHR) {
            $('#inject-event-creation-modal').empty().append(data);
        },
    });
}

function loadEventUpdateModal() {
    $.ajax({
        url: "/load-event-update-modal/",
        type: "GET",
        dataType: 'html',
        data:
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data, textStatus, jqXHR) {
            $('#inject-event-update-modal').empty().append(data);
        },
    });
}

function loadImportantAndUpcoming() {

    $.ajax({
        url: "/load-important-and-upcoming/",
        type: "GET",
        dataType: 'html',
        data:
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data, textStatus, jqXHR) {
            $('#important-and-upcoming-list').empty().append(data);
        },

    });
}

// Store the month lengths & names
var month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    month_names = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July',
                   'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'],
    month_names_long = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                   'August', 'September', 'October', 'November', 'December'];

// Do not ask me to explain this function because I don't want to spend an hour re-learning it.
this.getWeekString = function() {
    var viewDate = getViewDate();
        viewDate.setDate(viewDate.getDate() - viewDate.getDay()),
        weekSunday = viewDate.getDate(),
        monthNum1 = viewDate.getMonth() + 1;
        
        // Add 6 days to get the following Saturday
        viewDate.setDate(viewDate.getDate() + 6);

    var weekSaturday = viewDate.getDate(),
        monthNum2 = viewDate.getMonth() + 1;

    // Return a string in the followin format: "7/1 - 7/7"
    return monthNum1 + "/" + weekSunday + " - " + monthNum2 + "/" + weekSaturday;
}

// Returns the date object holding the date of the calendar day appearing in slot 0 of 42 of this month.
getCalFirstDay = function() {
    var now = getViewDate();
        day = now.getDate();
        month = now.getMonth();
        year = now.getFullYear();

    now.setDate(1);

    var firstDayInt = now.getDay(),
        prevDays = firstDayInt == 0 ? 7 : firstDayInt;

    if(prevDays == 0) {
        // Return the first of the month
        return now;
    }

    var preMonth = month == 0 ? 11 : month - 1,
        preYear = preMonth == 11 ? year - 1 : year,
        preCurrentDay = month_length[preMonth] - prevDays + 1;

    // Check previous month for leap days 
    if(month == 2) {
        if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
            preCurrentDay = 29 - prevDays + 1;
        }
    }

    return dateTracker = new Date(preYear, preMonth, preCurrentDay);
}

// Returns the date string in a python friendly format: 2015-11-27, for example
getFullDateString = function(date) {
    var monthPadding = date.getMonth() < 9 ? "0" : "";

    return date.getFullYear() + "-" + monthPadding + (date.getMonth() + 1) + "-" + date.getDate();
}

/*  
    Fills in the mini-calendar specified table within the planner layout.

    @param year
        The year in XXXX format (i.e. 2015)
    @param month
        The month of the year (January = 0, December = 11)
    @param day
        The day of the week (Monday = 0, Sunday = 6)

    @note
        Use no parameters to use the current viewDate stored in sessionStorage

    #TODO --> Be able to click on days and then update the cal/viewDate to that day.
*/
this.miniCal = function() {
    this.html = "";

    // Returns the html (assuming it has been previously generated)
    this.getHTML = function() {
        return this.html;
    }

    // Updates the calendar to the current view date
    this.handleDateChange = function() {
        this.generateHTML();
        document.getElementById("planner-mini-calendar").innerHTML = this.getHTML();
    }

    // Creates the html of the calendar.
    this.generateHTML = function() {
        var now = getViewDate(),
            day = now.getDate(),
            month = now.getMonth(),
            year = now.getFullYear();

        var monthLength = month_length[month];

        // Quick check to compensate for leap years
        if(month == 1) {
            if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
                monthLength = 29;
            }
        }

        var firstDay = new Date(year, month, 1), 
            firstDayInt = firstDay.getDay(),
            lastDay = new Date(year, month, monthLength),
            lastDayInt = lastDay.getDay(),

            // Variable to store the html that we'll write to the document
            html = '<table class="planner-mini-calendar">' +
                        '<col><col><col><col><col><col><col>',

            // Store information about pre & post months & how many days we need to fill
            prevDays = firstDayInt == 0 ? 7 : firstDayInt,
            postDays = lastDayInt == 6 ? 7: 6 - lastDayInt;

        // Get the first day to display (it might be in a different month)
        var dayTracker = getCalFirstDay();        
        
        // Loop for 6 weeks always (max number needed for the longest month)
        for(var calWeek = 0; calWeek < 6; calWeek++) {
            // If we're in the current week, highlight it.
            if((day - now.getDay() == dayTracker.getDate() && prevDays != 7) ||
               (calWeek == 0 && day - now.getDay() < 1)) {
                html += '<tr class="planner-mini-calendar-active">';
            }
            else {
                html += '<tr>';
            }

            // Loop for 7 days (7 days per week)
            for(var calDay = 0; calDay < 7; calDay++) {
                // Make each date clickable to change the date
                html += '<td onclick="selectDate(' + 
                            dayTracker.getFullYear() + ', ' + 
                            dayTracker.getMonth() + ', ' + 
                            dayTracker.getDate() + ')"';

                // Previous month filler days
                if(calWeek == 0 && prevDays > 0) {
                    // Custom borders if it's the last preDay
                    var style = prevDays == 1 ? 'class="planner-mini-calendar-inactive-last"' :
                                                'class="planner-mini-calendar-inactive"';
                    html += style;
                    prevDays--;
                }
                // Post month filler days
                else if(postDays > 0 && dayTracker.getMonth() != month) {
                    html += 'class="planner-mini-calendar-inactive"';
                }
                
                // Close the td bracket & put the date in, & update the date
                html += '>' + dayTracker.getDate() + '</td>';
                dayTracker.setDate(dayTracker.getDate() + 1);
            }
            html += '</tr>';
        }
        // Store the generated html in our variable defined at class level
        this.html = html + '</table>';
    }
} 

// Returns the date of the specified day in the week
getDateOfDay = function(day) {
    var date = getViewDate(),
        monthPadding = "";

    date.setDate(date.getDate() - date.getDay() + day);

    if(date.getMonth() + 1 <= 9) {
        monthPadding = "0";
    }

    // Return the date string ("2015-11-21" for example)
    return date.getFullYear() + "-" + monthPadding + (date.getMonth() + 1) + "-" + date.getDate();
}

// Checks every category/date combination & hides events that are overflow (more than 4 events in one block)
hideOverflowEvents = function(layoutType) {
    var contentBlocks,
        spillSize,
        monthPadder;

    switch(layoutType) {
        case "DAY":
            throw "Day view shouldn't use this method...check please.";
            break;
        case "WEEK":
            contentBlocks = $(".planner-week-event-container");
            spillSize = 4;
            monthPadder = 0;
            break;
        case "MONTH":
            contentBlocks = $(".planner-month-event-container");
            spillSize = 5;
            monthPadder = 1;
            break;
        default:
            throw "Invalid parameter in hideOverflowEvents().";
    }

    // For every event block, check if it's over capacity and fix those that are.
    for(var i = 0; i < contentBlocks.length; i++) {
        var events = contentBlocks[i].getElementsByTagName('td');

        if(events.length > spillSize) {
            var eventNames = [],
                numEvents = 0,
                color = [];

            // Get the original style for the "+ X more" box
            color[0] = events[0].className;

            // Loop through the extra blocks & get their names
            for(var j = spillSize - 1; j < events.length; j) {
                // Store the event
                eventNames[numEvents] = $.trim(events[j].innerHTML);
                // Store the event's color
                color[numEvents + 1] = events[j].className;
                events[j].parentNode.remove();

                numEvents++;
            }

            // Append the box to say how many events are hidden
            var moreBox = "" +
                "<tr>" +
                    "<td class=\"" + color[0] + "\">" +
                        "<div tabindex=\"0\" data-container=\"body\" data-trigger=\"focus\" data-toggle=\"popover\" " + getPopoverContent("Extra Events", eventNames, color) + ">" +
                            "+ " + numEvents + " more" +
                        "</div>" +
                    "</td>" +
                "</tr>"

            $(moreBox).insertAfter(events[2 + monthPadder].parentNode);
        }
    }

    $(function () {
        $('[data-toggle="popover"]').popover({ html: true });
    })
}

getPopoverContent = function(title, events, color) {
    if(events.length < 1) {
        throw "No events to populate popover content."
    }
    else {
        var html = "<div class=\"event-popover-container\">";

        for(var i = 0; i < events.length; i++) {
            // Change the "/about/" section to a descriptive link to edit the event
            // Should connect with a modal trigger, but we're going to have to pull 
            // category data, date data, and probably some other fields.
            html += "<div class=\"event-popover-event " + color[i + 1] + "\">" + events[i] + "</div>";
        }

        html += "</div>";

        return "data-title='" + title + "' data-content='" + html + "'";
    }
}