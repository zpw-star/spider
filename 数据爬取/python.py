import os
import csv
import time
import datetime
import requests
from DrissionPage import ChromiumPage
from typing import List, Dict
import json

USER_INFO_CSV_PATH = "douyin_users_info.csv"


def get_user_info(page: ChromiumPage, user_url: str) -> Dict[str, str]:
    """
    爬取博主信息（昵称、身份认证、粉丝数、排名认证），并保存到CSV表格
    """
    try:
        # 启动用户信息接口监听
        page.listen.start('/aweme/v1/web/user/profile/')
        page.get(user_url)
        resp = page.listen.wait()

        if not resp:
            print(f"未捕获到用户信息接口响应（URL：{user_url}）")
            return {}

        # 解析用户数据
        data = resp.response.body
        user_data = data.get('user', {})
        if not user_data:
            print(f"未找到用户信息（URL：{user_url}）")
            return {}

        # 提取用户信息
        nickname = user_data.get('nickname', '未知博主')
        followers_count = user_data.get('mplatform_followers_count', 0)  # 粉丝数

        # 身份认证
        account_cert = '未知'
        try:
            account_cert_str = user_data.get('account_cert_info', '{}')
            account_cert = json.loads(account_cert_str).get('label_text', '未知')
        except:
            pass

        # 排名认证
        rank_label = '未知'
        try:
            rank_data = user_data.get('profile_rank_label', {})
            rank_label = rank_data.get('text', '未知')
        except:
            pass


        # 保存博主信息到CSV文件名（douyin_users_info.csv）
        save_user_info_to_csv({
            '用户主页': user_url,
            '昵称': nickname,
            '身份认证': account_cert,
            '粉丝数': followers_count,
            '排名认证': rank_label
        })

        return {
            "nickname": nickname,
            "account_cert": account_cert,
            "followers_count": followers_count,
            "rank_label": rank_label
        }

    except Exception as e:
        print(f"获取用户信息失败（URL：{user_url}）：{e}")
        if page.listen.running:
            page.listen.stop()
        return {}


def save_user_info_to_csv(user_info: Dict):
    """保存用户信息到 CSV表格"""
    fieldnames = ['用户主页', '昵称', '身份认证', '粉丝数', '排名认证']

    # 检查文件是否存在，不存在则创建并写入表头
    file_exists = os.path.exists(USER_INFO_CSV_PATH)

    with open(USER_INFO_CSV_PATH, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(user_info)

    print(f"用户信息已保存到表格：{USER_INFO_CSV_PATH}")


def save_video(video_url: str, video_folder: str, video_id: str) -> None:
    """
    下载视频到指定文件夹（用视频ID命名）
    :param video_url: 视频播放链接
    :param video_folder: 视频保存目录
    :param video_id: 视频ID（用于文件名）
    """
    try:
        os.makedirs(video_folder, exist_ok=True)  # 创建文件夹（若不存在）
        video_path = os.path.join(video_folder, f"{video_id}.mp4")

        # 使用固定的headers，包含必要的Cookie和Referer
        headers = {
            'cookie': 'enter_pc_once=1; UIFID_TEMP=c4a29131752d59acb78af076c3dbdd52744118e38e80b4b96439ef1e20799db0a2522d3700d5f8b4c11fd3ccc880a13218e921e636ae59e0d1329770e970f45a0e00dfea5fe10b5cd18ec2f1d4d2397913c6c0f9f2bc908ac9b54d9b1591caa7; hevc_supported=true; dy_swidth=1707; dy_sheight=1067; WebUgChannelId=%2230023%22; s_v_web_id=verify_mftbcxhy_EN9hZMsu_gVYB_4qli_BMWn_S4BggxLD1OOU; fpk1=U2FsdGVkX19QIfQuR4zBKWyayO/TFnJbFTkAzoFskPpDMcsXeD52caYJSLdnClQwGeQVEBELZU6PEABMA57JyQ==; fpk2=f51bb482c660d0eeadd1f058058a2b35; xgplayer_user_id=690960224182; UIFID=c4a29131752d59acb78af076c3dbdd52744118e38e80b4b96439ef1e20799db00d637041f84e1ad0c6613e5637b227b4fb071906dca50506db49d64f13afb52a7c363c11f5705615623f6dcb21e660baf448ffb2296c1d8d90d700583fe1aabf2ee1ced0cfc37ae19b55a3d18c58717cee9d89144323b7f4b5cba03176c57231c3fcdc0abde8bc57af9f74a57cd017ef17432c7d62f0f7bc997532e654652a53; is_dash_user=1; __security_mc_1_s_sdk_crypt_sdk=e3aa73c8-48dd-956a; bd_ticket_guard_client_web_domain=2; passport_csrf_token=96313a54e47805104ad442ec1e016b6f; passport_csrf_token_default=96313a54e47805104ad442ec1e016b6f; SEARCH_RESULT_LIST_TYPE=%22single%22; my_rd=2; passport_assist_user=CkHmd0KvbyHvRDRzNzo0MxWEaQUPhHwf-VB0XwMLqwtiTtSWr3TpxSCz6dZFuJUhEMVp7hU66wpbQnTSBMZQvVCMnxpKCjwAAAAAAAAAAAAAT4H0A1dMkxAo7sH4z_OxIv0QzzRaUO_Z4b6mc8Bj8Zg7srZj0QHG-GLOySE-xVWUeU8QivD8DRiJr9ZUIAEiAQNL37PB; n_mh=vnQnlnSPy9gnciLIS9jPR8G9g1EMulpSZ2SjjyRYyv4; sid_guard=af8f8b1bb01e809ab086a75f2d682fc8%7C1758546723%7C5184000%7CFri%2C+21-Nov-2025+13%3A12%3A03+GMT; uid_tt=b778395ea18ab762287cce25496aabc5; uid_tt_ss=b778395ea18ab762287cce25496aabc5; sid_tt=af8f8b1bb01e809ab086a75f2d682fc8; sessionid=af8f8b1bb01e809ab086a75f2d682fc8; sessionid_ss=af8f8b1bb01e809ab086a75f2d682fc8; is_staff_user=false; sid_ucp_v1=1.0.0-KDE1ZWFmM2ZhMTFkZWY1Mzg3NTZiNDQ4MWRkZmExNTQ3YTYyZDUyMGUKIQiL_rDFyM2iBBCjlsXGBhjvMSAMMNiUoq4GOAdA9AdIBBoCbGYiIGFmOGY4YjFiYjAxZTgwOWFiMDg2YTc1ZjJkNjgyZmM4; ssid_ucp_v1=1.0.0-KDE1ZWFmM2ZhMTFkZWY1Mzg3NTZiNDQ4MWRkZmExNTQ3YTYyZDUyMGUKIQiL_rDFyM2iBBCjlsXGBhjvMSAMMNiUoq4GOAdA9AdIBBoCbGYiIGFmOGY4YjFiYjAxZTgwOWFiMDg2YTc1ZjJkNjgyZmM4; _bd_ticket_crypt_cookie=492dbf7fa9cc20fbd38bee9674a98d6b; __security_mc_1_s_sdk_sign_data_key_web_protect=9fd38033-498f-9045; __security_mc_1_s_sdk_cert_key=dc9c8fd2-4c6b-bac7; __security_server_data_status=1; login_time=1758546722750; SelfTabRedDotControl=%5B%5D; publish_badge_show_info=%220%2C0%2C0%2C1759211216481%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; strategyABtestKey=%221759719942.824%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAOWl1z-Y0pgKuMy5jW9lLoPNrIy33xAOtTWDGkM8fqxrk1twS7qFG_jfoiOyYpVXs%2F1759766400000%2F0%2F1759720003629%2F0%22; playRecommendGuideTagCount=6; totalRecommendGuideTagCount=6; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; __ac_nonce=068e37beb008d6e052bd; __ac_signature=_02B4Z6wo00f01OhZYtgAAIDDdj3CSNAU3fzoeWZAAFL6d3; douyin.com; device_web_cpu_core=32; device_web_memory_size=8; architecture=amd64; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAOWl1z-Y0pgKuMy5jW9lLoPNrIy33xAOtTWDGkM8fqxrk1twS7qFG_jfoiOyYpVXs%2F1759766400000%2F0%2F1759738861952%2F0%22; xg_device_score=7.626993737609486; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A1067%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A32%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; session_tlb_tag=sttt%7C15%7Cr4-LG7AegJqwhqdfLWgvyP_________aGB84hbZ8O5ZtokjkRtLuEaacKNwBAuNXWXR35wUXYzQ%3D; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f2735353232333d3d36323c303234272927676c715a75776a716a666a69273f2763646976602778; bit_env=P_BQOLpGBysGCkAX6JZRveZM65yGSbSYoNYqgA3Wb7EAtCvm7F0PQtYEsMc454CxdNQeGO87gDNmK4xwYVPAVzZjZ0zZu2fkjunFzxZwjF5PZ_6iao8O8mAUECDwS5qg1TtTJ-BbT-v8w7NemQtQOw7keProImCXnv6gRidg6yzfbVXWo4B8z876x418rjrQp4lll0xYVhS75e1xM8OTCpAyusWb4XFhbubuOTvaC1oxBnLz8Be7ocXsWbGh-SAcVWk0tYmou-4-Pi-QFfMjz7r5FepMxMN1Lw9jEJRqJav9n9PFMsITRixle8eXu4rkLmErWoEBmqLC1lzz9uj5e0zqmXhGCuHY1tXeazBUURJtfq_2sHSkInUtyFS6VzYz6WHDal8jmtkwcRsRP0PXkZJvF2lb2lLfzUxVdgZ8LKdOzMqzFjSxtmKtmgjQFTT0tBoa-SbFmPdRzW9MpP9PJzcRBRczuLxUCNAKMbTz0XDfCMIL6yzjsE2UD3nCszdw; gulu_source_res=eyJwX2luIjoiNGEyZmE1ZTg5YTg1M2ViNDJiOTRmMzNjODI3MThlYzAyMDdmNDc5ZjdhYTgxNmE5ZjlmZmNjNmI3OGFhZWZmNiJ9; passport_auth_mix_state=45xya0yleesiy51l640xq5klq5tahyrkioc32n2xxmc1uirn; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSXNOcEZEMXd6c3NaVkVPTDBDVEFwVEYvelZva2dWZ0tzQlh0Z3hOWmJZa0Rldzkyb0JJL3YreG9VZzhXZlY4N2kwRk5SRFh6RVJXeFIxT2psT21CYVk9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; ttwid=1%7C92sza6Ovl7V4t47YCDkFbPzLgM1MLulKvYp5cL93fF8%7C1759738871%7C7af93352685fbb09bc8c6069db7aee07471714df7f77477ea3243928fd23dbab; biz_trace_id=95659391; odin_tt=0b3cfbce952eb418f1b5d76cb26dac904a1cc4b27e64330e51b43320076cadbf561b933826034e73f58fa38c222b9bc2c74d34cc6e3342027822075c06685e55; bd_ticket_guard_client_data_v2=eyJyZWVfcHVibGljX2tleSI6IkJJc05wRkQxd3pzc1pWRU9MMENUQXBURi96Vm9rZ1ZnS3NCWHRneE5aYllrRGV3OTJvQkkvdit4b1VnOFdmVjg3aTBGTlJEWHpFUld4UjFPamxPbUJhWT0iLCJ0c19zaWduIjoidHMuMi4wMDExYjE4MjE0NjlkMGNlZTZhYTI5N2U0ZjFiY2UzOGNmMmRlMjNkNzY4OWI0ZTc4ZmY1NDAwNzZmMmQzMzM4YzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiIvbHVZdEdveHVnOVk3SGg0em1pTGFyMVFxUVVjclhrMEpJUDZ6RklLN3ZZPSIsInNlY190cyI6IiNVSUZHdGYvQkdwbGJ4SnUrb0owY3FFaUYvOXFPNDJnSnlTaTVrMFI5eGhsT3ViVEZycjMxZ0VGQk8wcDUifQ%3D%3D; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22',
            'referer': 'https://www.douyin.com/user/MS4wLjABAAAAompXkPoYOGsA152dqYoytKycjIZ_aCCxHwGmLX5IsDM?from_tab_name=main',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        # 发送请求，获取视频内容
        video_content = requests.get(url=video_url, headers=headers).content

        # 数据保存
        with open(video_path, 'wb') as f:
            f.write(video_content)

        print(f"视频保存成功：{video_path}")
    except Exception as e:
        print(f"视频保存失败（ID：{video_id}）：{e}")


def save_video_stats(stats_csv_path: str, video_stats: Dict) -> None:
    """
    保存视频统计数据到博主专属CSV（昵称+stats）
    :param stats_csv_path: CSV文件路径（如：张三_stats.csv）
    :param video_stats: 视频统计数据（包含描述、点赞、转发等）
    """
    fieldnames = ['视频ID', '描述','话题标签', '发布时间', '视频链接', '点赞量', '转发量', '收藏量', '评论量', '推荐量', '时长']
    try:
        # 检查文件是否存在，不存在则写表头
        file_exists = os.path.exists(stats_csv_path)
        with open(stats_csv_path, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            # 填充行数据（确保所有字段有值）
            row = {key: video_stats.get(key, '未知') for key in fieldnames}
            writer.writerow(row)
        print(f"视频统计数据保存成功：{video_stats['视频ID']}")
    except Exception as e:
        print(f"统计数据保存失败（ID：{video_stats.get('视频ID', '未知')}）：{e}")


def crawl_video_comments(page: ChromiumPage, video_id: str, comments_folder: str) -> None:
    """
    爬取单个视频的评论，保存到博主文件夹的`comments`子目录
    :param page: 复用的浏览器实例
    :param video_id: 视频ID
    :param comments_folder: 评论保存目录（如：张三_video/comments）
    """
    try:
        video_url = f"https://www.douyin.com/video/{video_id}"  # 视频页面URL
        page.listen.start('aweme/v1/web/comment/list/')  # 启动评论接口监听
        page.get(video_url)  # 访问视频页面

        # 评论CSV文件路径（如：张三_video/comments/123456_comments.csv）
        comments_csv_path = os.path.join(comments_folder, f"{video_id}_comments.csv")
        fieldnames = ['昵称', '地区', '时间', '评论']

        # 初始化CSV（写表头）
        if not os.path.exists(comments_csv_path):
            with open(comments_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

        # 循环获取所有评论（处理分页）
        has_more = 1
        while has_more:
            resp = page.listen.wait(timeout=10)
            if not resp:
                print(f"未捕获到评论数据（视频ID：{video_id}）")
                break

            # 解析评论数据
            json_data = resp.response.body
            comments = json_data.get('comments', [])
            has_more = json_data.get('has_more', 0)

            # 保存评论到CSV
            with open(comments_csv_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                for comment in comments:
                    writer.writerow({
                        '昵称': comment.get('user', {}).get('nickname', '未知'),
                        '地区': comment.get('ip_label', '未知地区'),
                        '时间': datetime.datetime.fromtimestamp(comment.get('create_time', 0)).strftime(
                            '%Y-%m-%d %H:%M:%S') if comment.get('create_time') else '无时间',
                        '评论': comment.get('text', '无评论')
                    })

            print(f"评论保存成功（视频ID：{video_id}，当前页评论数：{len(comments)}）")
            # 滚动页面加载下一页（用scroll.to_see）
            if has_more:
                tab = page.ele('.Rcc71LyU')
                page.scroll.to_see(tab)
                time.sleep(2)

        page.listen.stop()
        print(f"视频评论爬取完成：{video_id}")
    except Exception as e:
        print(f" 评论爬取失败（视频ID：{video_id}）：{e}")
        page.listen.stop()


def crawl_user_videos(page: ChromiumPage, user_url: str, max_videos: int, user_info: Dict) -> None:
    """
    处理单个用户的所有视频：获取列表、保存视频、保存统计数据、爬取评论
    :param page: 复用的浏览器实例
    :param user_url: 用户主页URL
    :param max_videos: 每个博主爬取的视频数量限制
    :param user_info: 博主信息（昵称、身份认证）
    """
    try:
        nickname = user_info.get('nickname', '未知博主')
        # 替换昵称中的非法字符（避免创建文件夹失败）
        safe_nickname = nickname.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?',
                                                                                                                  '_').replace(
            '"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        # 博主文件夹结构：{昵称}_video/
        # ├── videos/ （保存视频，用ID命名）
        # ├── comments/ （保存评论，用视频ID命名CSV）
        # └── {昵称}_stats.csv （保存视频统计数据）
        user_folder = f"{safe_nickname}_video"
        video_folder = os.path.join(user_folder, 'videos')
        comments_folder = os.path.join(user_folder, 'comments')
        stats_csv_path = os.path.join(user_folder, f"{safe_nickname}_stats.csv")

        # 创建文件夹（若不存在）
        os.makedirs(video_folder, exist_ok=True)
        os.makedirs(comments_folder, exist_ok=True)

        # 启动视频列表接口监听（抖音用户主页视频接口）
        page.listen.start('/aweme/v1/web/aweme/post/')
        page.get(user_url)  # 访问用户主页

        video_count = 0  # 视频计数器（控制爬取数量）
        has_more = 1  # 是否有下一页（1=有，0=无）

        while has_more and video_count < max_videos:
            resp = page.listen.wait(timeout=10)
            if not resp:
                print(f" 未捕获到视频数据（用户：{nickname}）")
                break

            # 解析视频列表数据
            json_data = resp.response.body
            aweme_list = json_data.get('aweme_list', [])
            has_more = json_data.get('has_more', 0)

            # 遍历当前页视频
            for item in aweme_list:
                if video_count >= max_videos:
                    break

                # 提取视频核心信息
                video_id = item.get('aweme_id', '未知')
                desc = item.get('desc', '无描述')
                tag=item.get('caption','无标签')
                create_time = item.get('create_time')
                create_time_str = datetime.datetime.fromtimestamp(create_time).strftime(
                    '%Y-%m-%d %H:%M:%S') if create_time else '无时间'
                video_url = item.get('video', {}).get('play_addr', {}).get('url_list', [''])[0]  # 视频播放链接
                big_thumbs = item.get('video',{}).get('big_thumbs', [])
                duration = big_thumbs[0].get('duration')   # 视频时长（秒）

                # 提取统计数据（点赞、转发等）
                stats = item.get('statistics', {})
                video_stats = {
                    '视频ID': video_id,
                    '描述': desc,
                    '话题标签':tag,
                    '发布时间': create_time_str,
                    '视频链接': video_url,
                    '点赞量': stats.get('digg_count', 0),
                    '转发量': stats.get('share_count', 0),
                    '收藏量': stats.get('collect_count', 0),
                    '评论量': stats.get('comment_count', 0),
                    '推荐量': stats.get('recommend_count', 0),
                    '时长': f"{duration:.2f}秒" if duration else '未知时长'
                }

                # 保存视频到`videos`文件夹
                save_video(video_url, video_folder, video_id)
                # 保存统计数据到`{昵称}_stats.csv`
                save_video_stats(stats_csv_path, video_stats)
                # 爬取该视频的评论，保存到`comments`文件夹
                crawl_video_comments(page, video_id, comments_folder)

                video_count += 1  # 计数器递增

            # 滚动页面加载下一页（抖音视频需滚动触发）
            if has_more and video_count < max_videos:
                print(f"→ 正在加载下一页视频（用户：{nickname}，当前已爬：{video_count}条）")
                tab = page.ele('.Rcc71LyU')
                page.scroll.to_see(tab)
                time.sleep(2)

        print(f"用户视频处理完成（用户：{nickname}，共爬取：{video_count}条）")
    except Exception as e:
        print(f"用户视频处理失败（用户：{user_info.get('nickname', '未知')}）：{e}")


def main():
    # 用户列表（可自由增加/删减）
    user_urls = [
        "https://www.douyin.com/user/MS4wLjABAAAAprnLAzLSWusGfifK9oHcwLt6k9lXvj2PBCaCtgBiZ2kHfZGmjRLXCGFGxN2cEdhH?from_tab_name=main",

    ]
    # 每个博主爬取的视频,供测试用，不然数据量过大
    max_videos_per_user = int(input("请输入每个博主爬取的视频数量："))


    # 初始化浏览器（复用实例，避免多次启动）
    page = ChromiumPage()

    try:
        for user_url in user_urls:
            print(f"\n-------------------------- 开始处理用户：{user_url} --------------------------")
            # 获取用户信息（昵称、身份认证）
            user_info = get_user_info(page, user_url)
            if not user_info:
                print(f" 跳过用户：{user_url}（未获取到用户信息）")
                continue

            # 处理该用户的视频（保存、统计、评论）
            crawl_user_videos(page, user_url, max_videos_per_user, user_info)
            print(f"-------------------------- 用户处理完成：{user_url} --------------------------\n")
            time.sleep(5)
    except Exception as e:
        print(f"主程序错误：{e}")
    finally:
        # 关闭浏览器（释放资源）
        page.close()
        print("浏览器关闭")


if __name__ == "__main__":
    main()
