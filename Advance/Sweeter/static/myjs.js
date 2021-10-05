function toggle_like(post_id, type) {
    console.log(post_id, type)
    let $a_like = $(`#${post_id} a[aria-label=${type}]`)
    let $i_like = $a_like.find("i")

    let fa_class
    let fa_o_class
    switch(type) {
        case 'heart':
            fa_class = 'fa-heart'
            fa_o_class = 'fa-heart-o'
            break;
        case 'star':
            fa_class = 'fa-star'
            fa_o_class = 'fa-star-o'
            break;
        case 'thumbs-up':
            fa_class = 'fa-thumbs-up'
            fa_o_class = 'fa-thumbs-o-up'
            break;
    }

    if ($i_like.hasClass(fa_class)) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass(fa_o_class).removeClass(fa_class)
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass(fa_class).removeClass(fa_o_class)
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })

    }
}

function post() {
    let comment = $("#textarea-post").val()
    let today = new Date().toISOString()
    $.ajax({
        type: "POST",
        url: "/posting",
        data: {
            comment_give: comment,
            date_give: today
        },
        success: function (response) {
            $("#modal-post").removeClass("is-active")
            window.location.reload()
        }
    })
}

function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

function num2str(count) {
    if (count > 10000) {
        return parseInt(count / 1000) + "k"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "k"
    }
    if (count == 0) {
        return ""
    }
    return count
}

function get_posts(username) {
    if (username==undefined) {
        username=""
    }
    $("#post-box").empty()
    $.ajax({
        type: "GET",
        url: `/get_posts?username_give=${username}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let posts = response["posts"]
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    let time_post = new Date(post["date"])
                    let time_before = time2str(time_post)
                    // 하트
                    let class_heart = post['heart_by_me'] ? "fa-heart" : "fa-heart-o"
                    let count_heart = post['count_heart']
                    // 별
                    let class_star = post['star_by_me'] ? "fa-star" : "fa-star-o"
                    let count_star = post['count_star']
                    // 엄지
                    let class_thumbs_up = post['thumbs_up_by_me'] ? "fa-thumbs-up" : "fa-thumbs-o-up"
                    let count_thumbs_up = post['count_thumbs_up']

                    let html_temp = `<div class="box" id="${post["_id"]}">
                                                <article class="media">
                                                    <div class="media-left">
                                                        <a class="image is-64x64" href="/user/${post['username']}">
                                                            <img class="is-rounded" src="/static/${post['profile_pic_real']}"
                                                                 alt="Image">
                                                        </a>
                                                    </div>
                                                    <div class="media-content">
                                                        <div class="content">
                                                            <p>
                                                                <strong>${post['profile_name']}</strong> <small>@${post['username']}</small> <small>${time_before}</small>
                                                                <br>
                                                                ${post['comment']}
                                                            </p>
                                                        </div>
                                                        <nav class="level is-mobile">
                                                            <div class="level-left">
                                                                <!-- 하트 -->
                                                                <a class="level-item is-sparta" aria-label="heart" onclick="toggle_like('${post['_id']}', 'heart')">
                                                                    <span class="icon is-small"><i class="fa ${class_heart}"
                                                                                                   aria-hidden="true"></i></span>&nbsp;<span class="like-num">${num2str(count_heart)}</span>
                                                                </a>
                                                                <!-- 별 -->
                                                                <a class="level-item is-sparta" aria-label="star" onclick="toggle_like('${post['_id']}', 'star')">
                                                                    <span class="icon is-small"><i class="fa ${class_star}"
                                                                                                   aria-hidden="true"></i></span>&nbsp;<span class="like-num">${num2str(count_star)}</span>
                                                                </a>
                                                                <!-- 엄지 -->
                                                                <a class="level-item is-sparta" aria-label="thumbs-up" onclick="toggle_like('${post['_id']}', 'thumbs-up')">
                                                                    <span class="icon is-small"><i class="fa ${class_thumbs_up}"
                                                                                                   aria-hidden="true"></i></span>&nbsp;<span class="like-num">${num2str(count_thumbs_up)}</span>
                                                                </a>
                                                            </div>

                                                        </nav>
                                                    </div>
                                                </article>
                                            </div>`
                    $("#post-box").append(html_temp)
                }
            }
        }
    })
}