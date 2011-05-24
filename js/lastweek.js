control = {
  
  init: function() {
    
    console.log(data);
    
    //  Do the contents page
    $.each(data, function(key, story) {
      
      //  Grab the headline and put it on the contents page
      var dt = $('<dt>').addClass('headline').html(story['response']['content']['fields']['dow'] + ': ' + story['response']['content']['fields']['headline']);
      $('dl#contents').append(dt);
      var dd = $('<dd>').addClass('standfirst').html(story['response']['content']['fields']['standfirst']);
      $('dl#contents').append(dd);

    })
    
    //  Now do the stories

    $.each(data, function(key, story) {
      
      //  Grab the headline and put it on the contents page
      var storyHolder = $('<div>').addClass('storyHolder');
      var h3 = $('<h3>').addClass('headline').html(story['response']['content']['fields']['headline']);
      var body = $('<div>').addClass('story').html(story['response']['content']['fields']['body']);
      var a = $('<a>').attr('href', story['response']['content']['webUrl']).html(story['response']['content']['webUrl']);
      storyHolder.append(h3);
      storyHolder.append(body);
      storyHolder.append(a);
      $('div.main').append(storyHolder);

    })
    


  }

}