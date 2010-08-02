control = {
  
  display_review: function() {
    
    //  Attach events to objects
    $('div.news_holder_holder').click( function() {
      $('.news_holder_holder').css('display', 'none');
      $('.cover').css('display', 'block').animate({ opacity: 0.0 }, 333, function() {
        $('.cover').css('display', 'none');
      })
    })

    //  Now I want to go and loop thru all the data things and try and display them
    
    //  empty the contents
    $('div#review').html('');
    
    //  loop thru each story and throw the review in there.
    var new_width = 0;
    $.each(data, function(index, story) {
      console.log(story);
      var d = $('<div>');
      d.addClass('snippet');
      d.attr('id', hex_md5(story.response.content.apiUrl));
      d.css('position', 'absolute');
      d.css('top', '0px');
      d.css('left', new_width);
      d.click( function() {
        control.utils.show_story(story.response.content.apiUrl);
      });
      $('div#review').append(d);
      
      control.utils.write_article(story.response.content, hex_md5(story.response.content.apiUrl), 'short', 'fun');
      
      new_width += 320;
      new_width += 20;
      
    })
    
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

    write_article: function(content, target_div, article_length, reason) {
      
      if (target_div == null || article_length == null) {
        return;
      }
      
      if ($('div#' + target_div) == null) {
        return;
      }
      
      var new_html = ''
      new_html += '<h1><a href="' + content.webUrl + '">' + content.webTitle + '</a></h1>';
      
      //  if we are anything but just 'headline' then carry on
      if (article_length != 'headline') {
        new_html += '<p class="standfirst">' + content.fields.standfirst + '</p>';
        if (article_length != 'tiny') {
          new_html += '<p class="byline">' + content.fields.byline + '</p>';
          new_html += '<p class="place_date"><a href="http://' + content.fields.publication + '"> ' + content.fields.publication + '</a>, ';
          new_html += control.utils.formatDate(content.webPublicationDate) + '</p>';
          
          //  if we are anything other than short carry on
          if (article_length != 'short') {
            
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
            
            //  If we are medium length, just display the first para, otherwuise
            if (article_length == 'medium') {
              if ('body' in content.fields) {
                var new_body = content.fields.body.split('</p>');
                new_html += '<div class="body">' + new_body[0] + '</div><p class="more"><a href="' + content.webUrl + '">More</a> ...</p>';
              }
            } else if (article_length == 'full') {
              new_html += '<div class="body">' + content.fields.body + '</div>';
            }
          }
        }
      }
  
      $('div#' + target_div).html(new_html);            
      
    },

    show_story: function(apiUrl) {

      console.log(apiUrl);
      
      //  Now we need to get the correct content thing
      var content = null;
      $.each(data, function(index, story) {
        if (story.response.content.apiUrl == apiUrl) {
          control.utils.write_article(story.response.content, 'main_news', 'full', 'main');
        }
      })
  
      //  Get the pages whole height
      $('.cover').height($('body').height());
      $('.cover').css('display', 'block').animate({ opacity: 0.95 }, 666, function() {
        $('.news_holder_holder').css('display', 'block');
        // it's possible the story is now longer than the old body, so let's
        //  adjust it again.
        if ($('div.news_holder_holder').height() > $('body').height()) {
          $('.cover').height($('div.news_holder_holder').height()+10);
        }
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