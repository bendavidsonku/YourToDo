// Variable to keep track of which button (daily/weekly/...) was pressed last
var recurrenceSelectionTracker = null;

$(document).ready(function() {
    //The following function handles the reset of recurrence options when the "recurring" check box's value changes
    $('.event-creation-repeat-input').change(function() {
        if(this.checked)
        {
            $('#create-event-repeat-options-container').show();
            $('#event-creation-recurrence-duration-amount-text').prop('readonly', true);
            $('#event-creation-recurrence-duration-date-date').prop('readonly', true);
        }
        else
        {
            recurrenceSelectionTracker = null;
            $('#create-event-repeat-options-container').hide();
            $('#repeat-options').hide();
            $('.event-creation-recurrence-duration').hide();
            $('#create-event-monthly-repeat-choice-container').hide();
            resetAllMonthlyOptions();
            $('#create-event-weekly-repeat-choice-container').hide();
            resetAllWeeklyOptions();
            $('.create-event-repeat-event-occurance-dropdown-button').html('<span id="create-event-repeat-occurance-number-label" class="attribute-label">--</span><span class="caret"></span>');
            $('#event-creation-recurrence-explanation').hide();
            $('input[type=radio][name=recurrence-option]').prop('checked', false);
            $('#event-creation-recurrence-duration-amount-text').addClass('input-disabled');
            $('#event-creation-recurrence-duration-date-date').addClass('input-disabled');
            $('#event-creation-recurrence-duration-amount-text').prop('readonly', true);
            $('#event-creation-recurrence-duration-date-date').prop('readonly', true);
            $('#event-creation-recurrence-duration-amount-text').val("");
            $('#event-creation-recurrence-duration-date-date').val("");
        }
    });

    //The following function manages the radio button input options for recurrence options
    $('input[type=radio][name=recurrence-option]').change(function(){
        if ($('#event-creation-recurrence-duration-never').is(':checked'))
        {
            $('#event-creation-recurrence-duration-amount-text').prop('readonly', true);
            $('#event-creation-recurrence-duration-amount-text').addClass('input-disabled'); 
            $('#event-creation-recurrence-duration-date-date').prop('readonly', true);
            $('#event-creation-recurrence-duration-date-date').addClass('input-disabled');
            $('#event-creation-recurrence-duration-amount-text').val("");
            $('#event-creation-recurrence-duration-date-date').val("");
        }
        else if ($('#event-creation-recurrence-duration-amount-radio').is(':checked'))
        {
            $('#event-creation-recurrence-duration-amount-text').prop('readonly', false);
            $('#event-creation-recurrence-duration-amount-text').removeClass('input-disabled');
            $('#event-creation-recurrence-duration-date-date').prop('readonly', true);
            $('#event-creation-recurrence-duration-date-date').addClass('input-disabled');
            $('#event-creation-recurrence-duration-date-date').val("");
        }
        else if ($('#event-creation-recurrence-duration-date-radio').is(':checked'))
        {
            $('#event-creation-recurrence-duration-amount-text').prop('readonly', true);
            $('#event-creation-recurrence-duration-amount-text').addClass('input-disabled');
            $('#event-creation-recurrence-duration-date-date').prop('readonly', false);
            $('#event-creation-recurrence-duration-date-date').removeClass('input-disabled');
            $('#event-creation-recurrence-duration-amount-text').val("");
        }
    });

    //The following on click functions reset the necessary attributes in the modal
    $('#button-repeat-daily').click(function() {
        recurrenceSelectionTracker = 0;
        $('#repeat-options').show();
        $('.event-creation-recurrence-duration').show();
        $('#daily-repeat-options').show();
        $('#weekly-repeat-options').hide();
        resetAllWeeklyOptions();
        $('#create-event-weekly-repeat-choice-container').hide();
        $('#monthly-repeat-options').hide();
        resetAllMonthlyOptions();
        $('#create-event-monthly-repeat-choice-container').hide();
        $('#yearly-repeat-options').hide();
        $('.create-event-repeat-event-occurance-dropdown-button').html('<span id="create-event-repeat-occurance-number-label" class="attribute-label">--</span><span class="caret"></span>');
        $('#event-creation-recurrence-explanation').hide();
        $('input[type=radio][name=recurrence-option]').prop('checked', false);
        $('#event-creation-recurrence-duration-amount-text').addClass('input-disabled');
        $('#event-creation-recurrence-duration-date-date').addClass('input-disabled');
        $('#event-creation-recurrence-duration-amount-text').prop('readonly', true);
        $('#event-creation-recurrence-duration-date-date').prop('readonly', true);
        $('#event-creation-recurrence-duration-amount-text').val("");
        $('#event-creation-recurrence-duration-date-date').val("");
    });

    $('#button-repeat-weekly').click(function() {
        recurrenceSelectionTracker = 1;
        $('#repeat-options').show();
        $('.event-creation-recurrence-duration').show();
        $('#daily-repeat-options').hide();
        $('#weekly-repeat-options').show();
        $('#create-event-weekly-repeat-choice-container').show();
        $('#monthly-repeat-options').hide();
        resetAllMonthlyOptions();
        $('#create-event-monthly-repeat-choice-container').hide();
        $('#yearly-repeat-options').hide();
        $('.create-event-repeat-event-occurance-dropdown-button').html('<span id="create-event-repeat-occurance-number-label" class="attribute-label">--</span><span class="caret"></span>');
        $('#event-creation-recurrence-explanation').hide();
        $('input[type=radio][name=recurrence-option]').prop('checked', false);
        $('#event-creation-recurrence-duration-amount-text').addClass('input-disabled');
        $('#event-creation-recurrence-duration-date-date').addClass('input-disabled');
        $('#event-creation-recurrence-duration-amount-text').prop('readonly', true);
        $('#event-creation-recurrence-duration-date-date').prop('readonly', true);
        $('#event-creation-recurrence-duration-amount-text').val("");
        $('#event-creation-recurrence-duration-date-date').val("");
    });

    $('#event-creation-weekdays-checkbox').change(function() {
        $('#event-creation-mwf-checkbox').prop('checked', false);
        $('#event-creation-tr-checkbox').prop('checked', false);
        $('#event-creation-week-day-choice-sunday').prop('checked', false);
        $('#event-creation-week-day-choice-monday').prop('checked', false);
        $('#event-creation-week-day-choice-tuesday').prop('checked', false);
        $('#event-creation-week-day-choice-wednesday').prop('checked', false);
        $('#event-creation-week-day-choice-thursday').prop('checked', false);
        $('#event-creation-week-day-choice-friday').prop('checked', false);
        $('#event-creation-week-day-choice-saturday').prop('checked', false);

        if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--" && $('#event-creation-weekdays-checkbox').is(':checked'))
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur weekly, Monday through Friday');
            }
            else 
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks, Monday through Friday');
            }

            $('#event-creation-recurrence-explanation').show();
        }
        else if ($('event-creation-weekdays-checkbox').is(':checked') == false)
        {
            if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
            {
                repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur weekly');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks');
                }
            }
            else
            {
                $('#event-creation-recurrence-explanation').hide();
            }
        }
    });

    $('#event-creation-mwf-checkbox').change(function() {
        $('#event-creation-weekdays-checkbox').prop('checked', false);
        $('#event-creation-tr-checkbox').prop('checked', false);
        $('#event-creation-week-day-choice-sunday').prop('checked', false);
        $('#event-creation-week-day-choice-monday').prop('checked', false);
        $('#event-creation-week-day-choice-tuesday').prop('checked', false);
        $('#event-creation-week-day-choice-wednesday').prop('checked', false);
        $('#event-creation-week-day-choice-thursday').prop('checked', false);
        $('#event-creation-week-day-choice-friday').prop('checked', false);
        $('#event-creation-week-day-choice-saturday').prop('checked', false);

        if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--" && $('#event-creation-mwf-checkbox').is(':checked'))
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur weekly on Monday, Wednesday, and Friday');
            }
            else 
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks on Monday, Wednesday, and Friday');
            }

            $('#event-creation-recurrence-explanation').show();
        }
        else if ($('event-creation-mwf-checkbox').is(':checked') == false)
        {
            if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
            {
                repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur weekly');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks');
                }
            }
            else
            {
                $('#event-creation-recurrence-explanation').hide();
            }
        }
    });

    $('#event-creation-tr-checkbox').change(function() {
        $('#event-creation-weekdays-checkbox').prop('checked', false);
        $('#event-creation-mwf-checkbox').prop('checked', false);
        $('#event-creation-week-day-choice-sunday').prop('checked', false);
        $('#event-creation-week-day-choice-monday').prop('checked', false);
        $('#event-creation-week-day-choice-tuesday').prop('checked', false);
        $('#event-creation-week-day-choice-wednesday').prop('checked', false);
        $('#event-creation-week-day-choice-thursday').prop('checked', false);
        $('#event-creation-week-day-choice-friday').prop('checked', false);
        $('#event-creation-week-day-choice-saturday').prop('checked', false);

        if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--" && $('#event-creation-tr-checkbox').is(':checked'))
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur weekly on Tuesday and Thursday');
            }
            else 
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks on Tuesday and Thursday');
            }

            $('#event-creation-recurrence-explanation').show();
        }
        else if ($('event-creation-tr-checkbox').is(':checked') == false)
        {
            if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
            {
                repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur weekly');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks');
                }
            }
            else
            {
                $('#event-creation-recurrence-explanation').hide();
            }
        }
    });

    $('#event-creation-week-day-choice-sunday, #event-creation-week-day-choice-monday, #event-creation-week-day-choice-tuesday, #event-creation-week-day-choice-wednesday, #event-creation-week-day-choice-thursday, #event-creation-week-day-choice-friday, #event-creation-week-day-choice-saturday').change(function() {
        $('#event-creation-weekdays-checkbox').prop('checked', false);
        $('#event-creation-mwf-checkbox').prop('checked', false);
        $('#event-creation-tr-checkbox').prop('checked', false);
        weekdaySelectionCreator();
    });

    $('#button-repeat-monthly').click(function() {
        recurrenceSelectionTracker = 2;
        $('#repeat-options').show();
        $('.event-creation-recurrence-duration').show();
        $('#daily-repeat-options').hide();
        $('#weekly-repeat-options').hide();
        resetAllWeeklyOptions();
        $('#create-event-weekly-repeat-choice-container').hide();
        $('#monthly-repeat-options').show();
        $('#create-event-monthly-repeat-choice-container').show();
        $('#yearly-repeat-options').hide();
        $('.create-event-repeat-event-occurance-dropdown-button').html('<span id="create-event-repeat-occurance-number-label" class="attribute-label">--</span><span class="caret"></span>');
        $('#event-creation-recurrence-explanation').hide();
        $('input[type=radio][name=recurrence-option]').prop('checked', false);
        $('#event-creation-recurrence-duration-amount-text').addClass('input-disabled');
        $('#event-creation-recurrence-duration-date-date').addClass('input-disabled');
        $('#event-creation-recurrence-duration-amount-text').prop('readonly', true);
        $('#event-creation-recurrence-duration-date-date').prop('readonly', true);
        $('#event-creation-recurrence-duration-amount-text').val("");
        $('#event-creation-recurrence-duration-date-date').val("");
    });

    $('#event-creation-same-day-next-month-checkbox').change(function() {
        $('#event-creation-same-day-week-next-month-checkbox').prop('checked', false);

        if ($('#event-creation-same-day-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            if ($('.event-creation-date-input').val() != "")
            {
                repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());
                var tempString = $('.event-creation-date-input').val();
                tempString = dateParcer(tempString);

                if (repeatNumber == 1)
                {
                    if (tempString == "31")
                    {
                        $('#event-creation-recurrence-explanation').text('This event will occur monthly on the last day of the month');
                    }
                    else
                    {
                        $('#event-creation-recurrence-explanation').text('This event will occur monthly on day ' + tempString);
                    }
                }
                else
                {
                    if (tempString == "31")
                    {
                        $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months on the last day of the month');
                    }
                    else
                    {
                        $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months on day ' + tempString);
                    }
                }

                $('#event-creation-recurrence-explanation').show();
            }
        }
        else if (!$('#event-creation-same-day-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur monthly');
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months');
            }

            $('#event-creation-recurrence-explanation').show();
        }
        else if ($('#event-creation-same-day-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() == "--")
        {
            if ($('.event-creation-date-input').val() != "")
            {
                var tempString = $('.event-creation-date-input').val();
                tempString = dateParcer(tempString);

                if (tempString == "31")
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur on the last day of the month');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur on day ' + tempString + ' of the month');
                }

                $('#event-creation-recurrence-explanation').show();
            }
        }
    });

    $('#event-creation-same-day-week-next-month-checkbox').change(function() {
        $('#event-creation-same-day-next-month-checkbox').prop('checked', false);

        if ($('#event-creation-same-day-week-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            if ($('.event-creation-date-input').val() != "")
            {
                repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());
                var explanationInfo = findNthDayOfTheWeekInMonth($('.event-creation-date-input').val());

                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur monthly on the ' + explanationInfo[1] + ' ' + explanationInfo [0] + ' of the month');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber +' months on the ' + explanationInfo[1] + ' ' + explanationInfo [0] + ' of the month');
                }

                $('#event-creation-recurrence-explanation').show();
            }
        }
        else if (!$('#event-creation-same-day-week-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur monthly');
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months');
            }

            $('#event-creation-recurrence-explanation').show();
        }
        else if ($('#event-creation-same-day-week-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() == "--")
        {
            if ($('.event-creation-date-input').val() != "")
            {
                var explanationInfo = findNthDayOfTheWeekInMonth($('.event-creation-date-input').val());

                $('#event-creation-recurrence-explanation').text('This event will occur on the ' + explanationInfo[1] + ' ' + explanationInfo [0] + ' of the month');

                $('#event-creation-recurrence-explanation').show();
            }
        }
    });

    $('.event-creation-date-input').change(function() {

        if (recurrenceSelectionTracker == 2 && $('#event-creation-same-day-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());
            var tempString = $('.event-creation-date-input').val();
            tempString = dateParcer(tempString);

            if (repeatNumber == 1)
            {
                if (tempString == "31")
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur monthly on the last day of the month');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur monthly on day ' + tempString);
                }
            }
            else
            {
                if (tempString == "31")
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months on the last day of the month');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months on day ' + tempString);
                }
            }

            $('#event-creation-recurrence-explanation').show();
        }
        if (recurrenceSelectionTracker == 2 && $('#event-creation-same-day-week-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());
            var explanationInfo = findNthDayOfTheWeekInMonth($('.event-creation-date-input').val());

            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur monthly on the ' + explanationInfo[1] + ' ' + explanationInfo [0] + ' of the month');
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber +' months on the ' + explanationInfo[1] + ' ' + explanationInfo [0] + ' of the month');
            }

            $('#event-creation-recurrence-explanation').show();
        }
        if (recurrenceSelectionTracker == 2 && $('#event-creation-same-day-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() == "--")
        {
            var tempString = $('.event-creation-date-input').val();
                tempString = dateParcer(tempString);

            if (tempString == "31")
            {
                $('#event-creation-recurrence-explanation').text('This event will occur on the last day of the month');
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur on day ' + tempString + ' of the month');
            }

            $('#event-creation-recurrence-explanation').show();
        }
        if (recurrenceSelectionTracker == 2 && $('#event-creation-same-day-week-next-month-checkbox').is(':checked') && $('.create-event-repeat-event-occurance-dropdown-button').text() == "--")
        {
            var explanationInfo = findNthDayOfTheWeekInMonth($('.event-creation-date-input').val());

            $('#event-creation-recurrence-explanation').text('This event will occur on the ' + explanationInfo[1] + ' ' + explanationInfo [0] + ' of the month');
            $('#event-creation-recurrence-explanation').show();
        }
    });

    $('#button-repeat-yearly').click(function() {
        recurrenceSelectionTracker = 3;
        $('#repeat-options').show();
        $('.event-creation-recurrence-duration').show();
        $('#daily-repeat-options').hide();
        $('#weekly-repeat-options').hide();
        resetAllWeeklyOptions();
        $('#create-event-weekly-repeat-choice-container').hide();
        $('#monthly-repeat-options').hide();
        $('#create-event-monthly-repeat-choice-container').hide();
        resetAllMonthlyOptions();
        $('#yearly-repeat-options').show();
        $('.create-event-repeat-event-occurance-dropdown-button').html('<span id="create-event-repeat-occurance-number-label" class="attribute-label">--</span><span class="caret"></span>');
        $('#event-creation-recurrence-explanation').hide();
        $('input[type=radio][name=recurrence-option]').prop('checked', false);
        $('#event-creation-recurrence-duration-amount-text').addClass('input-disabled');
        $('#event-creation-recurrence-duration-date-date').addClass('input-disabled');
        $('#event-creation-recurrence-duration-amount-text').prop('readonly', true);
        $('#event-creation-recurrence-duration-date-date').prop('readonly', true);
        $('#event-creation-recurrence-duration-amount-text').val("");
        $('#event-creation-recurrence-duration-date-date').val("");
    });
});

// Event Drop Down Menu Function - replaces default value with user-specified value
$(function(){

    $('.dropdown-menu-create-event-parentCategory li a').click(function(){

      $(this).parents('#create-event-parentCategory-dropdown').find('.btn').html('<span class="attribute-label">' + $(this).text() +'</span></span><span class="caret"></span>');
    });

    $('.dropdown-menu-create-event-timeEstimate li a').click(function(){

        $(this).parents('#create-event-timeEstimate-dropdown').find('.btn').html('<span class="attribute-label">' + $(this).text() +'</span></span><span class="caret"></span>');
    });

    //This function assists in generating an explanation of how a user's event will occur
    $('.dropdown-menu-create-event-repeat-occurance-number li a').click(function(){

        $(this).parents('#create-event-repeat-occurance-number-dropdown').find('.btn').html('<span class="attribute-label">' + $(this).text() +'</span></span><span class="caret"></span>');

        var repeatNumber = parseInt($(this).text());

        if (recurrenceSelectionTracker == 0)
        {
            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur daily');
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' days');
            }

            $('#event-creation-recurrence-explanation').show();
        }
        if (recurrenceSelectionTracker == 1)
        {
            if (weekdaySelectionCreator() > 0)
            {
                // Let the function call from if-statement run and do nothing inside this 
            }
            else if ($('#event-creation-weekdays-checkbox').is(':checked'))
            {
                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur weekly, Monday through Friday');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks, Monday through Friday');
                }

                $('#event-creation-recurrence-explanation').show();
            }
            else if ($('#event-creation-mwf-checkbox').is(':checked'))
            {
                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur weekly on Monday, Wednesday, and Friday');
                }
                else 
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks on Monday, Wednesday, and Friday');
                }

                $('#event-creation-recurrence-explanation').show();
            }
            else if ($('#event-creation-tr-checkbox').is(':checked'))
            {
                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur weekly on Tuesday and Thursday');
                }
                else 
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks on Tuesday and Thursday');
                }

                $('#event-creation-recurrence-explanation').show();
            }
            else
            {
                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur weekly');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks');
                }

                $('#event-creation-recurrence-explanation').show();
            }
        }
        if (recurrenceSelectionTracker == 2)
        {
            if ($('#event-creation-same-day-next-month-checkbox').is(':checked'))
            {
                if ($('.event-creation-date-input').val() != "")
                {
                    var tempString = $('.event-creation-date-input').val();
                    tempString = dateParcer(tempString);

                    if (repeatNumber == 1)
                    {
                        if (tempString == "31")
                        {
                            $('#event-creation-recurrence-explanation').text('This event will occur monthly on the last day of the month');
                        }
                        else
                        {
                            $('#event-creation-recurrence-explanation').text('This event will occur monthly on day ' + tempString);
                        }
                    }
                    else
                    {
                        if (tempString == "31")
                        {
                            $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months on the last day of the month');
                        }
                        else
                        {
                            $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months on day ' + tempString);
                        }
                    }

                    $('#event-creation-recurrence-explanation').show();
                }
            }
            else if ($('#event-creation-same-day-week-next-month-checkbox').is(':checked'))
            {
                if ($('.event-creation-date-input').val() != "")
                {
                    var explanationInfo = findNthDayOfTheWeekInMonth($('.event-creation-date-input').val());
                    if (repeatNumber == 1)
                    {
                        $('#event-creation-recurrence-explanation').text('This event will occur monthly on the ' + explanationInfo[1] + ' ' + explanationInfo [0] + ' of the month');
                    }
                    else
                    {
                        $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber +' months on the ' + explanationInfo[1] + ' ' + explanationInfo [0] + ' of the month');
                    }

                    $('#event-creation-recurrence-explanation').show();
                }
            }
            else
            {
                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur monthly');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' months');
                }

                $('#event-creation-recurrence-explanation').show();
            }

        }
        if (recurrenceSelectionTracker == 3)
        {
            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur yearly');
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' years');
            }

            $('#event-creation-recurrence-explanation').show();
        }
    });
});

// Handles event creation AJAX form submission and validates form before .ajax call
$('#create-event-submit').click(function(){
    var eventName = $('.event-creation-name-input').val();
    var eventParentCategory = $('.event-parentCategory-dropdown-button').text();
    eventParentCategory = eventParentCategory.replace("Event's Category", "");
    var eventDescription = $('#event-creation-description-input').val();
    var eventDate = $('.event-creation-date-input').val();
    var eventTimeEstimate = $('.create-event-timeEstimate-dropdown-button').text();
    eventTimeEstimate = eventTimeEstimate.replace("Time Estimate", "");
    var eventStartTime = $('.event-creation-startTime-input').val();
    var eventEndTime = $('.event-creation-endTime-input').val();
    var eventImportant = $('.event-creation-important-input').is(':checked');
    var periodOfRecurrence = $('.create-event-repeat-event-occurance-dropdown-button').text();
    var recurrenceCheckBoxes = [];
    var recurrenceEndOptions = [];
    var nthOccuranceOfSelectedDate = "";
    var validForm = true;

    if (eventTimeEstimate == "Time Estimate")
    {
        eventTimeEstimate = "None";
    }
    if ((eventStartTime != "" && eventEndTime == "") || (eventStartTime == "" && eventEndTime != ""))
    {
        $('#create-event-error-message-1').hide();
        $('#create-event-error-message-2').fadeIn('fast').delay(3500).fadeOut('slow');
        validForm = false;
    }
    if ((eventName.length == 0 || eventParentCategory == "" || eventDate == "" || eventParentCategory == "Event's Category") && validForm != false)
    {
        $('create-event-error-message-2').hide();
        $('#create-event-error-message-1').fadeIn('fast').delay(3500).fadeOut('slow');
        validForm = false;
    }
    // Validation of recurring options
    if ($('.event-creation-repeat-input').is(':checked') && validForm != false)
    {
        var recurrenceDropdownValue = $('.create-event-repeat-event-occurance-dropdown-button').text();
        if (recurrenceDropdownValue == "--")
        {
            $('#create-event-error-message-1').fadeIn('fast').delay(3500).fadeOut('slow');
            validForm = false;
        }
        if (validForm)
        {
            switch(recurrenceSelectionTracker)
            {
                // Daily 
                case 0:
                    validForm = validateRecurrenceEnd(recurrenceEndOptions);
                    break;
                // Weekly
                case 1:
                    validForm = validateRecurrenceEnd(recurrenceEndOptions);
                    if (validForm != false)
                    {
                        for (var i = 0; i < 12; i++)
                        {
                            recurrenceCheckBoxes[i] = 0;
                        }
                        if ($('#event-creation-weekdays-checkbox').is(':checked'))
                        {
                            recurrenceCheckBoxes[0] = 1;
                        }
                        if ($('#event-creation-mwf-checkbox').is(':checked'))
                        {
                            recurrenceCheckBoxes[1] = 1;
                        }
                        if ($('#event-creation-tr-checkbox').is(':checked'))
                        {
                            recurrenceCheckBoxes[2] = 1;
                        }
                        if ($('#event-creation-week-day-choice-sunday').is(':checked'))
                        {
                            recurrenceCheckBoxes[3] = 1;
                        }
                        if ($('#event-creation-week-day-choice-monday').is(':checked'))
                        {
                            recurrenceCheckBoxes[4] = 1;
                        }
                        if ($('#event-creation-week-day-choice-tuesday').is(':checked'))
                        {
                            recurrenceCheckBoxes[5] = 1;
                        }
                        if ($('#event-creation-week-day-choice-wednesday').is(':checked'))
                        {
                            recurrenceCheckBoxes[6] = 1;
                        }
                        if ($('#event-creation-week-day-choice-thursday').is(':checked'))
                        {
                            recurrenceCheckBoxes[7] = 1;
                        }
                        if ($('#event-creation-week-day-choice-friday').is(':checked'))
                        {
                            recurrenceCheckBoxes[8] = 1;
                        }
                        if ($('#event-creation-week-day-choice-saturday').is(':checked'))
                        {
                            recurrenceCheckBoxes[9] = 1;
                        }
                    }
                    break;
                // Monthly
                case 2:
                    validForm = validateRecurrenceEnd(recurrenceEndOptions);
                    if (validForm != false)
                    {
                        for (var i = 0; i < 12; i++)
                        {
                            recurrenceCheckBoxes[i] = 0;
                        }
                        if ($('#event-creation-same-day-next-month-checkbox').is(':checked'))
                        {
                            recurrenceCheckBoxes[10] = 1;
                        }
                        if ($('#event-creation-same-day-week-next-month-checkbox').is(':checked'))
                        {
                            recurrenceCheckBoxes[11] = 1;
                            nthOccuranceOfSelectedDate = findNthDayOfTheWeekInMonth(eventDate)[2];
                        }
                    }
                    break;
                // Yearly
                case 3:
                    validForm = validateRecurrenceEnd(recurrenceEndOptions);
                    break;
                // No Choice
                case null:
                    validForm = false;
                    break;
            }
        }
    }
    // Pass in recurrence tracker in form that Python can understand
    if (recurrenceSelectionTracker == null)
    {
        recurrenceSelectionTracker = "None";
    }
    if (validForm)
    {
        $.ajax({
            url: '/create-event/',
            type: 'POST',
            dataType: 'html',
            data:
            {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                ajax_event_name: eventName,
                ajax_event_parentCategory: eventParentCategory,
                ajax_event_description: eventDescription,
                ajax_event_date: eventDate,
                ajax_event_timeEstimate: eventTimeEstimate,
                ajax_event_startTime: eventStartTime,
                ajax_event_endTime: eventEndTime,
                ajax_event_important: eventImportant,
                ajax_event_recurrence_type: recurrenceSelectionTracker,
                ajax_event_recurrence_checkbox_array: recurrenceCheckBoxes,
                ajax_event_period_of_recurrence: periodOfRecurrence,
                ajax_event_recurrence_end_options_array: recurrenceEndOptions,
                ajax_event_nth_occurrence_of_selected_date: nthOccuranceOfSelectedDate,
            },
            success: function(data, textStatus, jqXHR) {
                $('#ajax-create-event-modal').modal('hide');
                $('.modal-backdrop').remove();
                changeViewDate("NONE");
            },
            error: function() {
                
            },
        });
    }
});

// Handles reseting the event creation modal on close or create
$('#ajax-create-event-modal').on('hidden.bs.modal', function(){
    $('.event-creation-name-input').val("");
    $('.event-parentCategory-dropdown-button').html("<span class='attribute-label'>Event's Category</span><span class='caret'></span>");
    $('#event-creation-description-input').val("");
    $('.event-creation-date-input').val("");
    $('.create-event-timeEstimate-dropdown-button').html('<span class="attribute-label">Time Estimate</span><span class="caret"></span>');
    $('.event-creation-startTime-input').val("");
    $('.event-creation-endTime-input').val("");
    $('.event-creation-important-input').prop('checked', false);
    recurrenceSelectionTracker = null;
    $('.event-creation-repeat-input').prop('checked', false);
    $('#create-event-repeat-options-container').hide();
    $('#repeat-options').hide();
    $('.event-creation-recurrence-duration').hide();
    $('#weekly-repeat-options').hide();
    resetAllWeeklyOptions();
    $('#create-event-weekly-repeat-choice-container').hide();
    $('#monthly-repeat-options').hide();
    $('#create-event-monthly-repeat-choice-container').hide();
    resetAllMonthlyOptions();
    $('#yearly-repeat-options').hide();
    $('#create-event-error-message-1').hide();
    $('#create-event-error-message-2').hide();
    $('.create-event-repeat-event-occurance-dropdown-button').html('<span id="create-event-repeat-occurance-number-label" class="attribute-label">--</span><span class="caret"></span>');
    $('#event-creation-recurrence-explanation').hide();
    $('input[type=radio][name=recurrence-option]').prop('checked', false);
    $('#event-creation-recurrence-duration-amount-text').addClass('input-disabled');
    $('#event-creation-recurrence-duration-date-date').addClass('input-disabled');
    $('#event-creation-recurrence-duration-amount-text').val("");
    $('#event-creation-recurrence-duration-date-date').val("");
});

//The following function resets the necessary attributes in the modal
function resetAllWeeklyOptions() {
    $('#event-creation-weekdays-checkbox').prop('checked', false);
    $('#event-creation-mwf-checkbox').prop('checked', false);
    $('#event-creation-tr-checkbox').prop('checked', false);
    $('#event-creation-week-day-choice-sunday').prop('checked', false);
    $('#event-creation-week-day-choice-monday').prop('checked', false);
    $('#event-creation-week-day-choice-tuesday').prop('checked', false);
    $('#event-creation-week-day-choice-wednesday').prop('checked', false);
    $('#event-creation-week-day-choice-thursday').prop('checked', false);
    $('#event-creation-week-day-choice-friday').prop('checked', false);
    $('#event-creation-week-day-choice-saturday').prop('checked', false);
}

function resetAllMonthlyOptions() {
    $('#event-creation-same-day-next-month-checkbox').prop('checked', false);
    $('#event-creation-same-day-week-next-month-checkbox').prop('checked', false);
}

// Handles explanation display of custom selected days
function weekdaySelectionCreator() {

    var sunday = false;
    var saturday = false;
    var creationString = "";
    var multipleMarked = 0;

    if ($('#event-creation-week-day-choice-sunday').is(':checked'))
    {
        sunday = true;
        creationString = "Sunday|";
        multipleMarked++;
    }
    if ($('#event-creation-week-day-choice-monday').is(':checked'))
    {
        creationString = creationString + "Monday|";
        multipleMarked++;
    }
    if ($('#event-creation-week-day-choice-tuesday').is(':checked'))
    {
        creationString = creationString + "Tuesday|";
        multipleMarked++;
    }
    if ($('#event-creation-week-day-choice-wednesday').is(':checked'))
    {
        creationString = creationString + "Wednesday|";
        multipleMarked++;
    }
    if ($('#event-creation-week-day-choice-thursday').is(':checked'))
    {
        creationString = creationString + "Thursday|";
        multipleMarked++;
    }
    if ($('#event-creation-week-day-choice-friday').is(':checked'))
    {
        creationString = creationString + "Friday|";
        multipleMarked++;
    }
    if ($('#event-creation-week-day-choice-saturday').is(':checked'))
    {
        saturday = true;
        creationString = creationString + "Saturday|";
        multipleMarked++;
    }
    if (multipleMarked == 7)
    {
        if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());
            
            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every day');
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks, every day');
            }

            $('#event-creation-recurrence-explanation').show();
        }
    }
    else if (sunday == false && saturday == false && multipleMarked == 5)
    {
        if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur weekly, Monday through Friday');
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks, Monday through Friday');
            }

            $('#event-creation-recurrence-explanation').show();
        }
    }
    else
    {
        if ($('.create-event-repeat-event-occurance-dropdown-button').text() != "--")
        {
            repeatNumber = parseInt($('.create-event-repeat-event-occurance-dropdown-button').text());

            if (multipleMarked > 1)
            {
                for (i = 0; i < multipleMarked - 1; i++)
                {
                    if (i == multipleMarked - 2)
                    {
                        creationString = creationString.replace("|", " and ");
                    }
                    else
                    {
                        creationString = creationString.replace("|", ", ");
                    }
                }

                creationString = creationString.replace("|", "");
            }
            else if (multipleMarked == 1)
            {   
                creationString = creationString.replace("|", "");
            }
            if (repeatNumber == 1)
            {
                $('#event-creation-recurrence-explanation').text('This event will occur weekly on ' + creationString);
            }
            else
            {
                $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks on ' + creationString);
            }
            if (multipleMarked == 0)
            {
                if (repeatNumber == 1)
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur weekly');
                }
                else
                {
                    $('#event-creation-recurrence-explanation').text('This event will occur every ' + repeatNumber + ' weeks');
                }
            }
            else
            {
                $('#event-creation-recurrence-explanation').show();
            }
        }
    }

    return multipleMarked;
}

function dateParcer(date)
{
    returnDate = date.charAt(8);

    if (returnDate == "0")
    {
        return date.charAt(9);
    }
    else
    {
        return(date.charAt(8) + date.charAt(9));
    }
}

function findNthDayOfTheWeekInMonth(selectedDate)
{
    var year = selectedDate.substring(0,4);
    var month = selectedDate.substring(5,7);
    var day = selectedDate.substring(8,10);
    // Gives a Javascript date object of the date passed in as a parameter
    selectedDate = new Date(year, month - 1, day);
    // Gets "day identifying index" of the passed in date
    var selectedDay = selectedDate.getDay();
    // Gives a Javascript date object of the first day of the month of the date passed in as a parameter
    var dateTracker = new Date(year, month - 1, 1);
    // Gets first day of the month in the given "selectedDate"
    var dayTracker = new Date(year, month - 1, 1).getDay();
    // Gets how many days are in the month of the given "selectedDate"
    var daysInTheMonth = new Date(year, month, 0).getDate();
    var nthOccuranceOfSelectedDay = 0;

    for(i = 0; i < daysInTheMonth; i++)
    {
        if (selectedDay == dayTracker)
        {
            if (selectedDate.getTime() == dateTracker.getTime())
            {
                nthOccuranceOfSelectedDay++;
                break;
            }
            else 
            {
                nthOccuranceOfSelectedDay++;
            }
        }
        if (dayTracker == 6)
        {
            dayTracker = 0;
        }
        else
        {
            dayTracker++;
        }
        dateTracker.setDate(dateTracker.getDate() + 1);
    }

    var selectedDayArray = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var returnDay = selectedDayArray[selectedDay];
    var nthOccuranceOfSelectedDayArray = ["first", "second", "third", "fourth", "last"];
    var returnNthNumber = nthOccuranceOfSelectedDay;
    nthOccuranceOfSelectedDay = nthOccuranceOfSelectedDayArray[nthOccuranceOfSelectedDay - 1];
    var dayAndOccurance = [returnDay, nthOccuranceOfSelectedDay, returnNthNumber];
    return dayAndOccurance;
}

function validateRecurrenceEnd(recurrenceEndOptions) {
    if (!($('input[type=radio][name=recurrence-option]').is(':checked')))
    {
        $('#create-event-error-message-1').fadeIn('fast').delay(3500).fadeOut('slow');
        return false;
    }
    else
    {
        if ($('#event-creation-recurrence-duration-never').is(':checked'))
        {
            // No check is needed in this case & form is valid
            recurrenceEndOptions[0] = "never";
            return true;
        }
        else if ($('#event-creation-recurrence-duration-amount-radio').is(':checked'))
        {
            var contentInInput = $('#event-creation-recurrence-duration-amount-text').val();
            if (!isNaN(contentInInput))
            {
                if (!contentInInput || !(/\S/.test(contentInInput)))
                {
                    // Content is empty or only whitespace
                    $('#create-event-error-message-1').fadeIn('fast').delay(3500).fadeOut('slow');
                    return false;
                }
                else
                {
                    // Form is valid
                    recurrenceEndOptions[0] = "number";
                    recurrenceEndOptions[1] = contentInInput;
                    return true;
                }
            }
            else
            {
                $('#event-creation-recurrence-duration-amount-text').val("");
                $('#create-event-error-message-1').fadeIn('fast').delay(3500).fadeOut('slow');
                return false;
            }
        }
        else if ($('#event-creation-recurrence-duration-date-radio').is(':checked'))
        {
            if ($('#event-creation-recurrence-duration-date-date').val() == "")
            {
                // Date input hasn't been changed or is default value
                $('#create-event-error-message-1').fadeIn('fast').delay(3500).fadeOut('slow');
                return false;
            }
            else
            {
                // Form is valid
                recurrenceEndOptions[0] = "date";
                recurrenceEndOptions[1] = $('#event-creation-recurrence-duration-date-date').val();
                return true;
            }
        }
    }
}