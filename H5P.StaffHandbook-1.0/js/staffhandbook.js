var H5P = H5P || {};

H5P.StaffHandbook = (function ($) {
  /**
   * Constructor
   */
  function StaffHandbook(options, contentId) {
    this.$ = $(this);
    this.contentId = contentId;
    this.options = $.extend(true, {}, {
      handbookData: {
        title: "Personalhåndbog",
        subtitle: "Søgbar videnbase for ansatte",
        searchPlaceholder: "Søg i personalhåndbogen...",
        alphabetSections: []
      }
    }, options);
  }

  /**
   * Attach function called by H5P framework to insert H5P content into page
   */
  StaffHandbook.prototype.attach = function ($container) {
    var self = this;
    
    $container.addClass('h5p-staff-handbook');
    
    // Build HTML structure
    var html = '';
    html += '<div class="wiki-container">';
    html += '  <div class="wiki-header">';
    html += '    <h1>📚 ' + self.options.handbookData.title + '</h1>';
    html += '    <p>' + self.options.handbookData.subtitle + '</p>';
    html += '  </div>';
    
    // Search box
    html += '  <div class="search-container">';
    html += '    <div class="search-box">';
    html += '      <input type="text" id="searchInput" placeholder="' + self.options.handbookData.searchPlaceholder + '">';
    html += '      <span class="search-icon">🔍</span>';
    html += '    </div>';
    html += '  </div>';
    
    // Main content
    html += '  <div class="main-content" id="mainContent">';
    
    // Alphabet sections
    self.options.handbookData.alphabetSections.forEach(function(section) {
      html += '<div class="alphabet-section" data-letter="' + section.letter + '">';
      html += '  <h2>' + section.letter + '</h2>';
      
      // Articles
      section.articles.forEach(function(article) {
        html += '  <details class="article-details">';
        html += '    <summary>' + article.title + '</summary>';
        html += '    <div class="article-content">';
        
        // Subsections
        if (article.subsections && article.subsections.length > 0) {
          article.subsections.forEach(function(subsection) {
            html += '      <details class="subsection-details">';
            html += '        <summary>' + subsection.title + '</summary>';
            html += '        <div class="subsection-content">';
            html += subsection.content;
            html += '        </div>';
            html += '      </details>';
          });
        }
        
        html += '    </div>';
        html += '  </details>';
      });
      
      html += '</div>';
    });
    
    html += '  </div>'; // main-content
    html += '</div>'; // wiki-container
    
    $container.html(html);
    
    // Initialize search functionality
    self.initSearch($container);
  };

  /**
   * Initialize search functionality
   */
  StaffHandbook.prototype.initSearch = function($container) {
    var searchInput = $container.find('#searchInput');
    var mainContent = $container.find('#mainContent');
    var alphabetSections = $container.find('.alphabet-section');
    
    searchInput.on('input', function() {
      var searchTerm = $(this).val().toLowerCase().trim();
      
      if (searchTerm === '') {
        // Show all sections
        alphabetSections.removeClass('hidden');
        alphabetSections.find('.article-details').removeClass('hidden');
        
        // Remove "no results" message
        $container.find('.no-results').remove();
        return;
      }
      
      var hasResults = false;
      
      alphabetSections.each(function() {
        var section = $(this);
        var sectionHasResults = false;
        var articles = section.find('.article-details');
        
        articles.each(function() {
          var article = $(this);
          var articleText = article.text().toLowerCase();
          
          if (articleText.includes(searchTerm)) {
            article.removeClass('hidden');
            article.attr('open', ''); // Auto-open matching articles
            sectionHasResults = true;
            hasResults = true;
          } else {
            article.addClass('hidden');
          }
        });
        
        if (sectionHasResults) {
          section.removeClass('hidden');
        } else {
          section.addClass('hidden');
        }
      });
      
      // Show/hide "no results" message
      var noResults = $container.find('.no-results');
      
      if (!hasResults) {
        if (noResults.length === 0) {
          var noResultsHtml = '<div class="no-results">';
          noResultsHtml += '  <p>😔 Ingen resultater fundet for "<strong>' + searchTerm + '</strong>"</p>';
          noResultsHtml += '  <p style="font-size: 0.9em; margin-top: 10px;">Prøv et andet søgeord</p>';
          noResultsHtml += '</div>';
          mainContent.append(noResultsHtml);
        }
      } else {
        noResults.remove();
      }
    });
  };

  return StaffHandbook;
})(H5P.jQuery);
