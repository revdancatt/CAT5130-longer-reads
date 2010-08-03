control = {
  
  display_review: function() {
    
    //  Attach events to objects
    $('div.news_holder_holder').click( function() {
      $('.news_holder_holder').css('display', 'none');
      $('.cover').css('display', 'block').animate({ opacity: 0.0 }, 333, function() {
        $('.cover').css('display', 'none');
      })
    })

    //  Attach events to objects
    $('div.cover').click( function() {
      $('.news_holder_holder').css('display', 'none');
      $('.cover').css('display', 'block').animate({ opacity: 0.0 }, 333, function() {
        $('.cover').css('display', 'none');
      })
    })
    

    //
    //  Do the to be reviewed column
    //
    $('div#review').html('');
    $('div#review').append($('<h1>').addClass('main').html('Review Queue ' + data.length));
    
    //  loop thru each story and throw the review in there.
    $.each(data, function(index, story) {
      var d = $('<div>');
      d.addClass('preview');
      d.addClass('snippet');
      d.attr('id', hex_md5(story.response.content.apiUrl));
      d.click( function() {
        control.utils.show_story(story.response.content.apiUrl);
      });
      $('div#review').append(d);
      
      control.utils.write_preview(story.response.content, hex_md5(story.response.content.apiUrl));
            
    })
    

    //
    //  Do the queued column
    //
    $('div#queued').html('');
    $('div#queued').append($('<h1>').addClass('main').html('Queued stories ' + queued_data.length));
    
    //  loop thru each story and throw the review in there.
    $.each(queued_data, function(index, story) {
      var d = $('<div>');
      d.addClass('preview');
      d.addClass('snippet');
      d.attr('id', hex_md5(story.response.content.apiUrl));
      d.click( function() {
        control.utils.show_story(story.response.content.apiUrl);
      });
      $('div#queued').append(d);
      
      control.utils.write_preview(story.response.content, hex_md5(story.response.content.apiUrl));
            
    })
    
  },
  
  
  
  
  approve: function(apiUrl) {

    $.ajax({ url: "/api/lr.article.approve", data: {'apiUrl' : apiUrl}, complete: function(response){

      //  Now we need to find the slot that represents this story and remove it
      var hash_id = hex_md5(apiUrl);
      var stored_height = $('div#' + hash_id).height();
      $('div#' + hash_id).css('height', stored_height);
      $('div#' + hash_id).css('overflow', 'hidden');
      $('div#' + hash_id).css('display', 'block').animate({ opacity: 0.0 }, 666, function() {
        $('div#' + hash_id).animate({ height: 1 }, 333, function() {
          $('div#' + hash_id).css('display', 'none');
          //  Now remove the item and append it to the end of the queue column
          var d = $('div#' + hash_id).detach();
          d.css('display', 'block');
          d.css('height', stored_height);
          $('div#queued').append(d);
          d.animate({ opacity: 1.0 }, 666);

          //  remove it from the data array and into the queued_data array
          var new_array = []
          $.each(data, function(index, obj) {
            if (obj.response.content.apiUrl == apiUrl) {
              queued_data.push(obj);
            } else {
              new_array.push(obj);
            }
          })
          data = new_array;

          $('div#review h1.main').html('Review Queue ' + data.length);
          $('div#queued h1.main').html('Queued stories ' + queued_data.length);

        })
      })


    }})

  },
  
  
  
  unapprove: function(apiUrl) {

    $.ajax({ url: "/api/lr.article.unapprove", data: {'apiUrl' : apiUrl}, complete: function(response){

      //  Now we need to find the slot that represents this story and remove it
      var hash_id = hex_md5(apiUrl);
      var stored_height = $('div#' + hash_id).height();
      $('div#' + hash_id).css('height', stored_height);
      $('div#' + hash_id).css('overflow', 'hidden');
      $('div#' + hash_id).css('display', 'block').animate({ opacity: 0.0 }, 666, function() {
        $('div#' + hash_id).animate({ height: 1 }, 333, function() {
          $('div#' + hash_id).css('display', 'none');
          //  Now remove the item and append it to the end of the queue column
          var d = $('div#' + hash_id).detach();
          d.css('display', 'block');
          d.css('height', stored_height);
          $('div#review').append(d);
          d.animate({ opacity: 1.0 }, 666);
          
          //  remove it from the queued_data array and into the data array
          var new_array = []
          $.each(queued_data, function(index, obj) {
            if (obj.response.content.apiUrl == apiUrl) {
              data.push(obj);
            } else {
              new_array.push(obj);
            }
          })
          queued_data = new_array;

          $('div#review h1.main').html('Review Queue ' + data.length);
          $('div#queued h1.main').html('Queued stories ' + queued_data.length);

        })
      })


    }})

  },
  
  
  
  reject: function(apiUrl) {

    $.ajax({ url: "/api/lr.article.reject", data: {'apiUrl' : apiUrl}, complete: function(response){
      
      //  Now we need to find the slot that represents this story and remove it
      var hash_id = hex_md5(apiUrl);
      $('div#' + hash_id).css('height', $('div#' + hash_id).height());
      $('div#' + hash_id).css('overflow', 'hidden');
      $('div#' + hash_id).css('display', 'block').animate({ opacity: 0.0 }, 666, function() {
        $('div#' + hash_id).animate({ height: 1 }, 333, function() {
          $('div#' + hash_id).css('display', 'none');
        })
      })
      
      $('div#review h1.main').html('Review Queue ' + data.length);
      $('div#queued h1.main').html('Queued stories ' + queued_data.length);

    }})

  },
  
  
  //////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////
  //
  //  UTILS
  //
  //////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////

  utils: {




    write_preview: function(content, target_div) {
      
      if (target_div == null) {
        return;
      }
      
      if ($('div#' + target_div) == null) {
        return;
      }
      
      var new_html = ''
      new_html += '<h1>' + content.webTitle + '</h1>';
      
      //  if we are anything but just 'headline' then carry on
      new_html += '<p class="standfirst">'
      if ('thumbnail' in content.fields) {
        new_html += '<img class="thumbnail" src="' + content.fields.thumbnail + '" />'
      }
      new_html += content.fields.standfirst + '</p>';
      new_html += '<p class="byline">' + content.fields.byline + '</p>';
      new_html += '<p class="place_date">' + content.fields.publication + ', ';
      new_html += control.utils.formatDate(content.webPublicationDate) + '</p>';
      
      //  Check to see if there is a photo
      if ('mediaAssets' in content && content.mediaAssets[0].type == 'picture') {
        if (parseInt(content.mediaAssets[0].fields.width) >= 320) {
          new_html += '<img class="main" src="' + content.mediaAssets[0].file + '" />';
        } else {
          new_html += '<img class="main" src="' + content.mediaAssets[0].file + '" />';
        }
        if ('caption' in content.mediaAssets[0].fields) {
          new_html += '<p class="photo_caption">' + content.mediaAssets[0].fields.caption + '</p>';
        } else if ('credit' in content.mediaAssets[0].fields) {
          new_html += '<p class="photo_caption">' + content.mediaAssets[0].fields.credit + '</p>';
        }
      }
        
      $('div#' + target_div).html(new_html);            
      
    },




    write_article: function(content, target_div, article_length, reason) {
      
      if (target_div == null || article_length == null) {
        return;
      }
      
      if ($('div#' + target_div) == null) {
        return;
      }
      
      var new_html = ''
      new_html += '<h1>' + content.webTitle + '</h1>';
      new_html += '<p class="standfirst">' + content.fields.standfirst + '</p>';
      new_html += '<p class="byline">' + content.fields.byline + '</p>';
      new_html += '<p class="place_date">' + content.fields.publication + ', ';
      new_html += control.utils.formatDate(content.webPublicationDate) + '</p>';
      
      //  Check to see if there is a photo
      if ('mediaAssets' in content && content.mediaAssets[0].type == 'picture') {
        if (parseInt(content.mediaAssets[0].fields.width) >= 320) {
          new_html += '<img class="main" src="' + content.mediaAssets[0].file + '" />';
        } else {
          new_html += '<img class="main" src="' + content.mediaAssets[0].file + '" />';
        }
        if ('caption' in content.mediaAssets[0].fields) {
          new_html += '<p class="photo_caption">' + content.mediaAssets[0].fields.caption + '</p>';
        } else if ('credit' in content.mediaAssets[0].fields) {
          new_html += '<p class="photo_caption">' + content.mediaAssets[0].fields.credit + '</p>';
        }
      }
      
      //  The main content
      new_html += '<div class="body">' + content.fields.body + '</div>';
  
      //  Put it into the target
      $('div#' + target_div).html(new_html);            
      
    },




    show_story: function(apiUrl) {

      //  Now we need to get the correct content thing
      var content = null;
      var is_from = null;
      $.each(data, function(index, story) {
        if (story.response.content.apiUrl == apiUrl) {
          content = story.response.content;
          control.utils.write_article(content, 'main_news', 'full', 'main');
          is_from = 'review';
        }
      })
  
      
      if (content == null) {
        $.each(queued_data, function(index, story) {
          if (story.response.content.apiUrl == apiUrl) {
            content = story.response.content;
            control.utils.write_article(content, 'main_news', 'full', 'main');
            is_from = 'queued';
          }
        })
      }

      
      if (content == null) return;

      //
      //  And now add the extra details
      //  first get the wordcount
      //

      var word_count = 0;
      $.each($('div#main_news div.body p'), function(index, p) {
        word_count += $(p).html().split(' ').length;
      })
      var count_per_min = parseInt(word_count / content.fields.time_spent * 100)/100;
      var count_per_sec = parseInt(word_count / content.fields.time_spent / 60 * 100)/100;
      
      $('div#details').html('');
      var ul = $('<ul>');
      ul.append($('<li>').html('Zone: ' + content.sectionName));
      ul.append($('<li>').html('View Count: ' + content.fields.view_count));
      ul.append($('<li>').html('Percent: ' + content.fields.percent));

      //  The next three involve a little colour styling ... not the best way of
      //  doing this, but readable for the moment. I'll shorthand it later
      
      //  Show the time spent
      if (content.fields.time_spent >= 6.0) {
        ul.append($('<li>').html('Time Spend: ' + content.fields.time_spent).addClass('green'));
      } else {
        ul.append($('<li>').html('Time Spend: ' + content.fields.time_spent));
      }

      //  And the word count
      if (word_count >= 2000) {
        ul.append($('<li>').html('Word Count: ' + word_count).addClass('green'));
      } else if (word_count < 1000) {
        ul.append($('<li>').html('Word Count: ' + word_count).addClass('red'));
      } else {
        ul.append($('<li>').html('Word Count: ' + word_count));
      }
      
      //  And the count per min
      if (count_per_min < 200) {
        ul.append($('<li>').html('Words per min: ' + count_per_min).addClass('red'));
      } else {
        ul.append($('<li>').html('Words per min: ' + count_per_min));
      }
      
      if (count_per_sec < (200/60)) {
        ul.append($('<li>').html('Words per second: ' + count_per_sec).addClass('red'));
      } else {
        ul.append($('<li>').html('Words per second: ' + count_per_sec));
      }
      $('div#details').append(ul);
      
      
      //
      //  Lets grab the keywords
      //
      $('div#keywords').html('');
      var ul = $('<ul>');
      $.each(content.tags, function(index, tag) {
        if (tag.type == 'keyword') {
          ul.append($('<li>').html(tag.webTitle));
        }
      })
      $('div#keywords').append(ul);
      
      
      //
      //  Now add the actions
      //
      $('div#actions').html('');
      var ul = $('<ul>');
      
      if (is_from == 'review') {
        ul.append($('<li>').html('approve').click( function() {control.approve(apiUrl)}));
      } else {
        ul.append($('<li>').html('unapprove').click( function() {control.unapprove(apiUrl)}));
      }
      ul.append($('<li>').html('reject').click( function() {control.reject(apiUrl)}));
      ul.append($('<li>').append($('<a>').attr('href', content.webUrl).attr('target', '_blank').html('view original')));
      
      $('div#actions').append(ul);
      
      


      //  Get the pages whole height
      $('.cover').height($('body').height());
      $('.cover').css('display', 'block').animate({ opacity: 0.95 }, 666, function() {
        $('.news_holder_holder').css('display', 'block');
        // it's possible the story is now longer than the old body, so let's
        //  adjust it again.
        if ($('div.news_holder_holder').height() > $('body').height()) {
          $('.cover').height($('div.news_holder_holder').height()+10);
        }
        
        scroll(0,0);
        
      })

    },

    getDate: function(dt) {
      
      var d = dt.split('T')[0];
      var t = dt.split('T')[1];
      var year = d.split('-')[0];
      var month = d.split('-')[1];
      var day = d.split('-')[2];
      var hour = t.split(':')[0];
      var min = t.split(':')[1];
      var dt = new Date(year, month-1, day, hour, min);
      return dt;
      
    },
    
    formatDate: function(d) {
      
      if (typeof d == 'string') {
        d = this.getDate(d);
      }
      
      var day_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()];
      var date_of_month = d.getDate();
      var month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()];
      var year = d.getFullYear();
      return day_of_week + ' ' + date_of_month + ' ' + month + ' ' + year;

    }
  }
}