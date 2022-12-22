import folium

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from photon.forms import *
from photon.models import SubList, Category, Person, Camera
from .filters import SnapshotFilter, PortfolioFilter, CatSelectedFilter


class RegisterView(TemplateView):
    template_name = "photon/registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()
        reg = True

        if request.method == 'POST':
            form = RegisterForm(request.POST)

        if form.is_valid() and form.no_dublicate():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            User.objects.create_user(username, email, password)
            user = authenticate(request, username=username, email=email, password=password)
            login(request, user)

            proform = ProfileForm(instance=self.get_profile(request.user))
            profile = proform.save(commit=False)

            profile.user = request.user
            profile.nick = username
            profile.email = email

            profile.save()

            subs = SubList.objects.create(user=request.user)

            messages.success(request, "THOMAS приветствует Вас!\nЗаполните Ваш профиль до конца!")
            return redirect(reverse("edit_profile", kwargs={'nick': request.user.profile}))

        context = {
            'form': form,
            'register': reg,
            'cats': Category.objects.all()
        }

        return render(request, self.template_name, context)

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None


class LoginView(TemplateView):
    template_name = "photon/registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LoginForm(request.POST)

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            context = {
                'form': form
            }

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("feed"))
                else:
                    context['error'] = "Данный пользователь более неактивен!"
                    return render(request, self.template_name, context)
            else:
                context['error'] = "Такого логина и пароля не существует.\nЗарегистрируйтесь!"
                return render(request, self.template_name, context)

        form = LoginForm()
        lgn = True

        context = {
            'form': form,
            'login': lgn,
            'cats': Category.objects.all()
        }
        return render(request, self.template_name, context)


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


def show_profile(request, nick):
    selected_user = Profile.objects.get(nick=nick)
    user = request.user
    your_profile = True

    if user.profile != selected_user:
        your_profile = False
        info = selected_user

        try:
            subscription = SubList.objects.get(user=user).subscriptions.get(nick=selected_user)
        except:
            subscription = None

        subs = SubList.objects.get_or_create(user=selected_user.user)[0].subscriptions.all()

    else:
        info = request.user.profile
        subscription = None
        subs = SubList.objects.get_or_create(user=user)[0].subscriptions.all()

    context = {
        'selected_user': info,
        'sel_user_subs': subs,
        'subscription': subscription,
        'cats': Category.objects.all(),
        'your_profile': your_profile
    }

    return render(request, "photon/registration/profile.html", context)


class EditProfileView(TemplateView):
    template_name = "photon/registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            cameras = request.POST.get('cameras')

            if form.is_valid():
                form.instance.user = request.user
                form.save()
                form.save_m2m()

                new_pro = Profile.objects.all().order_by('-id').first()

                if new_pro:
                    for cam in cameras.split(', '):
                        gear = Camera.objects.get_or_create(brand=cam)
                        if not gear in new_pro.gear.all():
                            new_pro.gear.add(gear[0])

                messages.success(request, "Профиль успешно обновлен!")
                return redirect(reverse("profile", kwargs={'nick': request.user.profile}))

        context = {
            'form': form,
            'cats': Category.objects.all()
        }
        return render(request, self.template_name, context)

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None


def show_snap(request, pk):
    snap = Snapshot.objects.get(pk=pk)
    user = request.user

    location = [snap.lat, snap.lon]
    m = folium.Map(width=550, height=250, location=location, zoom_start=6)
    folium.Marker([snap.lat, snap.lon], tooltip=snap.country, popup=snap.city, icon=folium.Icon(color='purple')).add_to(
        m)
    output_file = "photon/templates/photon/blocks/map.html"
    m.save(output_file)

    your_profile = False
    try:
        selected_user = Profile.objects.get(nick=snap.author.profile)
    except Profile.DoesNotExist:
        context = {['error']: 'User does not exist.'}
        return redirect(request.META['HTTP_REFERER'], context)

    if user.is_authenticated:
        subscription = None
        your_profile = True

        if user.profile != selected_user:
            your_profile = False

    context = {
        "snap": snap,
        'cats': Category.objects.all(),
        'map': m,
        'your_profile': your_profile,
        'selected_user': selected_user
    }

    return render(request, 'photon/photo.html', context)


def edit_snap(request, pk):
    context = {}

    try:
        snap = Snapshot.objects.get(pk=pk)
    except:
        context['error'] = "Такой фотографии не существует!"
        return redirect(request.META['HTTP_REFERER'], context)

    if request.method == 'POST':
        form = SnapshotForm(request.POST, request.FILES, instance=snap)
        all = request.POST.get('person_list').split(', ')

        if form.is_valid():
            pro = form.save(commit=False)
            pro.author = request.user

            pro.save()
            form.save_m2m()

            for p in all:
                psn = Person.objects.get_or_create(name=p)[0]
                if not psn in snap.person.all():
                    snap.person.add(psn)

            return redirect(reverse("show_snap", kwargs={'pk': pk}))
    else:
        form = SnapshotForm(instance=snap)

    return render(request, "photon/upload_snap.html", {'form': form})


def delete_snap(request, pk):
    context = {}

    try:
        snap = Snapshot.objects.get(pk=pk)
    except:
        context['error'] = "Такой фотографии не существует!"
        return redirect(request.META['HTTP_REFERER'], context)

    snap.delete()

    return redirect(reverse("portfolio", kwargs={'nick': request.user.profile}))


class UploadSnapView(TemplateView):
    template_name = 'photon/upload_snap.html'

    def dispatch(self, request, *args, **kwargs):
        form = SnapshotForm()

        if request.method == 'POST':
            form = SnapshotForm(request.POST, request.FILES)
            cat = request.POST.get('category')
            all = request.POST.get('person_list').split(', ')

            if form.is_valid():
                pro = form.save(commit=False)
                pro.author = request.user

                pro.save()
                form.save_m2m()

                new_snap = Snapshot.objects.all().order_by('-timestamp').first()

                for p in all:
                    psn = Person.objects.get_or_create(name=p)[0]
                    if not psn in new_snap.person.all():
                        new_snap.person.add(psn)

        context = {
            'form': form,
            'cats': Category.objects.all()
        }
        return render(request, self.template_name, context)


def show_portfolio(request, nick):
    context = {}
    user = request.user

    if user.is_authenticated:
        try:
            selected_user = Profile.objects.get(nick=nick)
        except Profile.DoesNotExist:
            context['error'] = 'User does not exist.'
            return redirect(request.META['HTTP_REFERER'], context)

        subscription = None
        your_profile = True

        if user.profile != selected_user:
            your_profile = False
            try:
                subscription = SubList.objects.filter(Q(user=user) & Q(subscriptions=selected_user))
            except:
                subscription = None

        snaps = Snapshot.objects.filter(author=selected_user.user)
        snap_filter = PortfolioFilter(request.GET, queryset=snaps)

        context = {
            'selected_user': selected_user,
            'subscription': subscription,
            'snaps': snaps,
            'your_profile': your_profile,
            'snap_filter': snap_filter,
            'cats': Category.objects.all()
        }

    else:
        context['error'] = 'Please, register!'
        return redirect(reverse("login"))

    return render(request, "photon/portfolio.html", context)


class FeedView(TemplateView):
    template_name = 'photon/feed.html'

    def dispatch(self, request, *args, **kwargs):
        context = {}

        snaps = Snapshot.objects.all().order_by('-timestamp')
        subs = None

        if not request.user.is_authenticated:
            snaps = snaps.filter(author__profile__private=False)
            guest = True

        else:
            guest = None
            subs = SubList.objects.get(user=request.user)
            snaps = snaps.filter(Q(author__profile__in=subs.subscriptions.all())
                                 | Q(category__name__in=subs.categories.all())
                                 | Q(camera__brand__in=subs.cameras.all())).distinct().order_by('-timestamp')

        snap_filter = SnapshotFilter(request.GET, queryset=snaps)

        context = {
            'snaps': snaps,
            'snap_filter': snap_filter,
            'guest': guest,
            'cats': Category.objects.all(),
            'subs': subs
        }
        return render(request, self.template_name, context)


def show_subs(request, nick):
    context = {}
    profile = Profile.objects.get(nick=nick)

    try:
        subs = SubList.objects.get(user=profile.user)
    except:
        context['error'] = "Ошибка списка подписок!"
        subs = None

    context = {
        'subs': subs,
        # 'user': user,
        'cats': Category.objects.all()
    }
    return render(request, "photon/subs.html", context)


def show_cats(request, cat_slug=None):
    context = {}
    user = request.user
    snaps, cats, cat_filter, subscription, ct = None, None, None, None, None

    if cat_slug:
        try:
            ct = Category.objects.get(slug=cat_slug)
            snaps = Snapshot.objects.filter(category=ct).order_by('-timestamp')
            cats = Category.objects.all()
            cat_filter = CatSelectedFilter(request.GET, queryset=snaps)
        except:
            context['error'] = 'Данной категории не существует!'
            return redirect(request.META['HTTP_REFERER'], context)

        try:
            subscription = SubList.objects.filter(Q(user=user) & Q(categories=ct))
        except:
            subscription = None

    elif request.method == 'POST':
        new_cat = request.POST.get('new_category')
        Category.objects.create(name=new_cat)
        context = {'message': "Категория успешно создана"}
        return render(request, "photon/cats.html", context)

    else:
        cats = Category.objects.all()

    context = {
        'cats': cats,
        'snaps': snaps,
        'snap_filter': cat_filter,
        'cat_slug': cat_slug,
        'subscription': subscription,
        'cat_name': ct.name
    }

    return render(request, "photon/cats.html", context)


def unsubscribe_pro(request, nick):
    selected_user = Profile.objects.get(nick=nick)
    SubList.objects.get(user=request.user).subscriptions.remove(selected_user)

    return redirect(request.META['HTTP_REFERER'])


def unsubscribe_cat(request, cat_slug):
    selected_cat = Category.objects.get(slug=cat_slug)
    SubList.objects.get(user=request.user).categories.remove(selected_cat)

    return redirect(request.META['HTTP_REFERER'])


def subscribe_pro(request, nick):
    f = Profile.objects.get(nick=nick)
    SubList.objects.get(user=request.user).subscriptions.add(f)

    return redirect(request.META['HTTP_REFERER'])


def subscribe_cat(request, cat_slug):
    ct = Category.objects.get(slug=cat_slug)
    SubList.objects.get(user=request.user).categories.add(ct)

    return redirect(request.META['HTTP_REFERER'])


class SearchView(TemplateView):
    template_name = 'photon/search.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if request.method == 'GET':
            query = request.GET.get("q")

            if len(query) > 0:
                search_pro = Profile.objects.filter(Q(nick__icontains=query)
                                                    | Q(fio__icontains=query)
                                                    | Q(city__icontains=query)
                                                    ).distinct()
                search_snap = Snapshot.objects.filter(Q(description__icontains=query)
                                                      | Q(city__icontains=query)
                                                      | Q(region__icontains=query)
                                                      | Q(country__icontains=query)
                                                      ).distinct()
                search_cat = Category.objects.filter(name__icontains=query)
                search_cam = Camera.objects.filter(brand__icontains=query)
                search_pers = Person.objects.filter(name__icontains=query)
                total = search_pro.count() + search_snap.count() + search_cat.count() + search_cam.count() + search_pers.count()
            else:
                return redirect(request.META['HTTP_REFERER'])

            context = {
                'cats': Category.objects.all(),
                'total': total,
                'profiles': search_pro,
                'snaps': search_snap,
                'categories': search_cat,
                'cameras': search_cam,
                'people': search_pers,
            }
            return render(request, self.template_name, context)
