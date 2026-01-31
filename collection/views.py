from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import PokemonCard, Binder
from .utils import search_card
import math

# Create your views here.
# Create your views here.
def index(request):
    return render(request, "collection/index.html")

def binder_shelf(request):
    binders = Binder.objects.order_by('-created_at')
    return render(request, "collection/binder_shelf.html", {'binders': binders})

@require_http_methods(["POST"])
def create_binder(request):
    name = request.POST.get('name')
    if name:
        binder = Binder.objects.create(name=name)
        # Redirect to the cover of the new binder
        return redirect('binder_cover', binder_id=binder.id)
    return redirect('binder_shelf')

def search_cards(request):
    query = request.GET.get('q', '')
    cards = search_card(query)
    return render(request, 'collection/partials/search_results.html', {'cards': cards})

@require_http_methods(["POST"])
def add_card(request, binder_id):
    binder = get_object_or_404(Binder, pk=binder_id)
    
    # Get card data from form (we'll implement this form in the result item)
    name = request.POST.get('name')
    card_id = request.POST.get('card_id')
    image_url = request.POST.get('image_url')
    set_name = request.POST.get('set_name')
    
    # Create card and assign to this binder
    PokemonCard.objects.create(
        binder=binder,
        name=name,
        card_id=card_id,
        image_url=image_url,
        set_name=set_name
    )
    
    # Return to the binder view (or trigger a refresh)
    # Ideally find which page the new card landed on, but defaulting to last page is okay for MVP
    # For now, just go to the open binder (Page 1)
    return redirect('binder_page', binder_id=binder.id, page=1)

def binder(request, binder_id, page=1):
    current_binder = get_object_or_404(Binder, pk=binder_id)

    # Check if this is a request for the Search Modal
    if request.htmx and request.GET.get('modal') == 'true':
         return render(request, 'collection/partials/search_modal.html', {'binder': current_binder})

    # Fetch Real Cards for this Binder
    all_cards = list(PokemonCard.objects.filter(binder=current_binder))
    
    # Pagination Logic
    # Page 0: Cover (No cards)
    # Page 1: 9 cards (Right side only)
    # Page 2+: 18 cards (Left and Right sides)
    
    if page == 0:
        # Cover View
        context = {
            'binder': current_binder,
            'page': 0,
            'is_cover': True,
            'is_first_page': False,
            'slots': [],
            'total_pages': 0, # Placeholder
            'has_next': True,
            'has_previous': False,
            'next_page': 1,
            'previous_page': None,
        }
        # Calculate Total Pages for context (same formula)
        total_cards = len(all_cards)
        if total_cards <= 9:
            context['total_pages'] = 1
        else:
            remaining = total_cards - 9
            context['total_pages'] = 1 + math.ceil(remaining / 18)
            
        return render(request, "collection/binder.html", context)

    if page == 1:
        start_index = 0
        end_index = 9
        slots_needed = 9
    else:
        # Page 1 took 9 cards.
        # Page 2 starts at 9, ends at 9 + 18 = 27
        # Page 3 starts at 27, ends at 27 + 18 = 45
        start_index = 9 + (page - 2) * 18
        end_index = start_index + 18
        slots_needed = 18
        
    # Get the cards for this page
    page_cards = all_cards[start_index:end_index]
    
    # Padding Logic: Fill the rest of the page with None if we run out of cards
    # This ensures the 3x3 grid always looks like a grid, just with empty slots
    filled_slots = len(page_cards)
    empty_slots_needed = max(0, slots_needed - filled_slots)
    
    current_slots = page_cards + [None] * empty_slots_needed
    
    # Calculate Total Pages
    total_cards = len(all_cards)
    if total_cards <= 9:
        total_pages = 1
    else:
        # Subtract first 9, then divide remainder by 18, round up
        remaining = total_cards - 9
        total_pages = 1 + math.ceil(remaining / 18)

    context = {
        'binder': current_binder,
        'page': page,
        'slots': current_slots,
        'is_cover': False,
        'is_first_page': (page == 1),
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_previous': True, # Page 1 can go back to 0
        'next_page': page + 1,
        'previous_page': page - 1 if page > 1 else 0,
    }
    
    return render(request, "collection/binder.html", context)
